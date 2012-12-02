#!/usr/bin/env python

from SimpleCV import *
from time import sleep



cam = Camera()
last = None

while True:
	sleep(.5)
	
	img = cam.getImage()
	img = img.findHaarFeatures('face.xml')
	try:
		img = img.sortArea()[-1].crop()
	except:
		continue
	
	faces = img.crop( 0, 0, img.width/2, img.height ).findHaarFeatures('right_eye.xml')
	if not faces:
		continue
	
	eye = faces[-1].crop().scale(5.0)
	eye = eye.crop( 0, int(eye.height*0.40), eye.width, int(eye.height*0.60) )
	eye = eye.crop( int(eye.width*0.15), int(eye.height*0.15), int(eye.width*0.70), int(eye.height*0.70) )
	
	if last is not None:
		try:
			m = eye.findMotion( last, 10, 'LK', True )
			m.draw()
			m = m[0]
			eye.dl().text(str(m.dx) + ', ' + str(m.dy),(0,0),color=Color.RED)
		except:
			pass
	
	last = eye
	
	eye.show()