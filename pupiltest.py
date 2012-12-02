#!/usr/bin/env python

from SimpleCV import *
from time import sleep



cam = Camera()

while True:
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
	
	try:
		for iris in eye.findCircle(50, 1, 50).sortColorDistance( Color.GREEN ):
			if iris.notOnImageEdge(1):
				direction = 'Centre'
				
				if iris.x < int( eye.width * 0.20 ):
					direction = 'East'
				elif iris.x > int( eye.width * 0.80 ):
					direction = 'West'
				elif iris.y < int( eye.height * 0.4 ):
					y = 'North'
				elif iris.y > int( eye.height * 0.6 ):
					y = 'South'
				
				eye.dl().text(direction,(0,0),color=Color.RED)
				break
	except:
		pass
	
	eye.show()
