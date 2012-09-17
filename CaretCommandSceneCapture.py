#!/usr/bin/python

## PREFACE ##
# Written by Maarten Mennes at the 2012 BrainHack
# 
##

import os, glob, subprocess, shutil, argparse, sys, datetime, time


##-----------------------------------------------------------------------------
parser = argparse.ArgumentParser(
                    description='''Script to create caret surface overlays in an automagical fashion.''')

# required options                    
reqoptions = parser.add_argument_group('Required Arguments')
reqoptions.add_argument('-specfile', action="store", dest="specfile", required=True, help='FULL path to the specfile you want to use, e.g., /home/caret/CARET_TUTORIAL_SEPT06/PALS_B12.BOTH-HEMS.INFL.73730.spec')
reqoptions.add_argument('-scenefile', action="store", dest="scenefile", required=True, help='FULL path to the scenefile, e.g., /Users/mennem01/Documents/NeuroBureau/2012_BrainHack/24hourPaper/24HourScene.scene !WARNING! You need to create this scenefile beforehand, which means you need to make at least one figure manually.')
reqoptions.add_argument('-ipr', action="store", dest="ipr", required=True, help='''
Number of Images you want Per Row. 
This is related to the number of viewing windows you have specified in your scene and how you want to layout these windows in your figure, e.g., if you have 4 viewing windows in your scene and -ipr 1 then your final image will contain window 1, 2, 3, 4 on one line. Setting -ipr 2 will give you 1, 2 / 3, 4 as your final configuration''')
reqoptions.add_argument('items', nargs='+', help='niftifiles')
reqoptions.add_argument('-template', action="store", dest="template", required=True, help='word to change in xml scene')


# optional options
optoptions = parser.add_argument_group('Optional Arguments')
optoptions.add_argument('-sn', action="store", dest="scenenumber", required=False, default='1', help='Scenenumber. Numerical index of the specific scene you want to use, e.g., if you saved the following scenes in your scenefile [lateral, medial, somethingelse], lateral would be 1, medial 2 and somethingelse 3. Check the order of the scenes in caret by loading the scenefile.')
optoptions.add_argument('-outprefix', action="store", dest="outprefix", default='', required=False, help='')
optoptions.add_argument('-outsuffix', action="store", dest="outsuffix", default='', required=False, help='')

# parse arguments
args = parser.parse_args()

##-----------------------------------------------------------------------------
specfile = args.specfile
scenefile = args.scenefile
imperrow = args.ipr
scenenumber = args.scenenumber
items = args.items
outprefix = args.outprefix
outsuffix = args.outsuffix
template = args.template


## subfunctions

# Open the scenefile and replace a placeholder by the needed image
# template = what you will replace
# replacement = what you want to replace it with
# a new, updated scene file will be created called XXXXX_adj.scene
def update_scene(scenefile, template, replacement):
	# use regula expressions to update the newscenefile
	import re

	# read in the scenefile
	oldscene = open(scenefile).read()

	# initialize newscenefile, open the newscenefile and write the update scene information to it
	newscenefile = scenefile.split('.scene')[0] + '_adj.scene'
	o = open(newscenefile,"w")
	o.write( re.sub(template,replacement,oldscene)  )
	o.close()
	
	return newscenefile


# open specfile, load the newscenefile and a predefined scene. Save the image(s) from the scene, with N images per row
def show_scene(specfile, scenefile, scenenumber, outputimage, imperrow):
	import subprocess
	cmd = ['caret_command', '-show-scene', specfile, scenefile, scenenumber, '-image-file', outputimage, str(imperrow)]
	print cmd
	subprocess.call(cmd)
	return


# Loop over .nii.gz images you specified at the command line
for i in items:
	print 'rendering item', i
	# update scene xml
	newscenefile = update_scene(scenefile,template,i)
	# render image
	# i are .nii.gz files
	# create outputimage name
	outname = i.split('.nii.gz')[0] + outsuffix + '.png'
	outputimage = os.path.join(outprefix, outname)
	print os.path.join(os.path.dirname(scenefile),newscenefile)
	show_scene(specfile,os.path.join(os.path.dirname(scenefile),newscenefile),scenenumber,outputimage,imperrow)
	
	