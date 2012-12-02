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
	eye.smooth("gaussian",(3,3), 2, grayscale = True)
	
	try:
		blob1 = BlobMaker()
		blobs = blob1.extractFromBinary(eye.invert().binarize(180).invert(),eye)
		
		if(len(blobs)>0):
			#blobs[0].drawHull(color=(0, 255, 0), alpha=-1, width=-1, layer=None)
			blobs[0].drawOutline(color=(255, 0, 0), alpha=-1, width=1, layer=None)
			radius = blobs[0].radius()
	except:
		pass
	
	eye.show()
