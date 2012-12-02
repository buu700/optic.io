#!/usr/bin/env python

from SimpleCV import *
from time import sleep



cam = Camera()

while True:
	sleep(.1)
	
	img = cam.getImage()
	img = img.findHaarFeatures('face.xml')
	try:
		img = img.sortArea()[-1].crop()
	except:
		continue
	
	faces = img.crop( 0, 0, img.width/2, img.height ).findHaarFeatures('right_eye.xml')
	if not faces:
		continue
	
	eye = faces[-1].crop().scale(5.0).grayscale()
	eye = eye.crop( 0, eye.height/5, eye.width, int(eye.height*0.8) )
	eye = eye.smooth("gaussian",(3,3), 2, grayscale = True).invert().binarize().invert()
	
	try:
		for iris in eye.findCircle(10, 10, 50).sortDistance().sortArea().sortColorDistance(Color.WHITE):
			if iris.crop().width < eye.width/3 and iris.crop().width > eye.width/3.5:
				iris.draw()
				break
	except:
		pass
	
	eye.show()
