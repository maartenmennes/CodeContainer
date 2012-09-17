


specfile = '/Users/Shared/caret/CARET_TUTORIAL_SEPT06/PALS_B12.BOTH-HEMS.INFL.73730.spec'
scenefile = '/Users/mennem01/Documents/NeuroBureau/2012_BrainHack/24hourPaper/24HourScene.scene'
ImagesPerRow = 1



# open specfile, load a predefined scene and save the image, with N images per row
def show_scene(specfile, scenefile, scene, outputimage, ImagesPerRow):
	import subprocess
	cmd = 'caret_command -show-scene ' + specfile + ' ' + scenefile + ' ' + scene + ' -image-file ' + outputimage + ' ' + str(ImagesPerRow)
	print cmd
	subprocess.call(cmd,shell=True)
	return


# update scenefile
def update_scene(scenefile, template, replacement):
	# regular expression change text
	import re
	newscenefile = scenefile.split('.scene')[0] + 'New.scene'
	o = open(newscenefile,"w")
	data = open(scenefile).read()
	o.write( re.sub(template,replacement,data)  )
	o.close()
	
	return newscenefile


# map volume to surface
# space = FLIRT, SPM2, SPM5
def map_volume_to_surface(,StereoSpace,):
	import subprocess
	cmd = 'caret_command -volume-map-to-surface-pals ${output} ${output} $s LEFT ${interp} ${infile} -metric-afm' %(StereoSpace)
	subprocess.call(cmd,shell=True)
	return


#nonzero
#scene = '3'
#scenename = 'unthr_M'
#template = 'PNAS_Smith090003.nii.gz'
#repl='.'
#top5
scene = '4'
scenename = 'z23_M'
template = 'PNAS_Smith090003_top5.nii.gz'
repl = '_2.3.'

for i in range(0,9):
	print i
	replacement = template.replace('3_top5.',str(i)+repl)
	print replacement
	newscenefile = update_scene(scenefile,template,replacement)
	outputimage = '/Users/mennem01/Documents/NeuroBureau/2012_BrainHack/24hourPaper/' + str(i) + '_' + scenename + '.png'
	print outputimage
	show_scene(specfile,newscenefile,scene,outputimage,'1')
	
	