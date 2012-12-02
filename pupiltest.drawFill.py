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
	
	eye = faces[-1].crop().scale(5.0)
	eye = eye.crop( 0, int(eye.height*0.4), eye.width, int(eye.height*0.6) )
	try:
		for iris in eye.findCircle(50, 1, 50).sortColorDistance(Color.GREEN):
			if iris.crop().width < eye.width/3.5 and iris.crop().width > eye.width/7.5 and iris.notOnImageEdge(10):
				eye.dl().circle( iris.coordinates(), 10, Color.RED, filled=True )
				eye.dl().text(str(iris.x) + ', ' + str(iris.y),(0,0),color=Color.RED)
				break
	except:
		pass
	
	eye.show()
