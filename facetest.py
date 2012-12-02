#!/usr/bin/env python

import SimpleCV


cam = SimpleCV.Camera()

while True:
	img = cam.getImage()
	faces = img.findHaarFeatures('face.xml')
	if faces:
		faces[-1].draw()
	img.show()
