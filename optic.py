#!/usr/bin/env python

import time
from SimpleCV import *
from pymouse import PyMouse
from numpy import array as vector





# http://code.opencv.org/projects/opencv/repository/revisions/master/changes/data/haarcascades/
FACE_CASCADE	= HaarCascade( "face.xml" )
EYE_CASCADE		= HaarCascade( "right_eye.xml" )
MOUTH_CASCADE	= HaarCascade( "mouth.xml" )
NOSE_CASCADE	= HaarCascade( "nose.xml" )



camera		= Camera()
blobMaker	= BlobMaker()
mouse		= PyMouse()



facePresent			= False
mouthWidth			= 0
nosePosition		= 0
distanceMouthNose	= 0
gaze				= None # x, y
mouseMoveData		= None # xPrime, yPrime, maxX, maxY

actionTriggered	= False
clickRegistered	= False



def Main():
	global FACE_CASCADE, EYE_CASCADE, MOUTH_CASCADE, NOSE_CASCADE, camera, blobMaker, mouse, facePresent, mouthWidth, nosePosition, distanceMouthNose, gaze, mouseMoveData, actionTriggered, clickRegistered
	
	
	# Event loop
	while True:
		time.sleep( 0.1 )
		
		image	= camera.getImage()
		
		try:
			face	= image.findHaarFeatures( FACE_CASCADE )[0]
		except:
			facePresent	= False
			continue
		
		try:
			# N.B. The enemy's gate is down (greater Y implies lower position on image)
			eye		= image.findHaarFeatures( EYE_CASCADE )[0]
			mouth	= image.findHaarFeatures( MOUTH_CASCADE )[0]
			nose	= image.findHaarFeatures( NOSE_CASCADE )[0]
			pupil	= Pupil( image )
			print pupil
			newMouthWidth			= mouth.width()
			newNosePosition			= nose.y
			newDistanceMouthNose	= mouth.maxY() - nose.minY()
			
			newGaze	= vector( eye.coordinates() ) - vector( pupil.coordinates()[0] )
		except:
			facePresent	= False
			continue
		
		
		
		if( facePresent is True ):
			print 'face.width: ' + str(face.width())
			print 'mouth.width: ' + str(mouth.width())
			print 'nose.y: ' + str(nose.y)
			print 'newMouthWidth: ' + str(newMouthWidth)
			print 'newNosePosition: ' + str(newNosePosition)
			print 'newDistanceMouthNose: ' + str(newDistanceMouthNose)
			
			# Enters mouse action decision tree if and only if mouth is puckered
			if( GreaterThan(mouthWidth, newMouthWidth, .01) is False ):
				mouseMoveData	= None
				actionTriggered	= False
				clickRegistered	= False
				continue
			elif( actionTriggered is False ):
				# Secondary calibration each time mouth puckers
				actionTriggered		= True
				nosePosition		= newNosePosition
				distanceMouthNose	= newDistanceMouthNose
				gaze				= newGaze
				continue
			
			print 'pucker'
			
			
			if( mouseMoveData is not None ):
				Move()
				clickRegistered	= False
			
			elif( GreaterThan(nosePosition, newNosePosition, .10, image.height) is True ):
				ScrollDown()
				clickRegistered	= False
			
			elif( GreaterThan(newNosePosition, nosePosition, .10, image.height) is True ):
				ScrollUp()
				clickRegistered	= False
			
			elif( GreaterThan(distanceMouthNose, newDistanceMouthNose, .05) is True and clickRegistered is False ):
				LeftClick()
				clickRegistered	= True
			
			elif( GreaterThan(newDistanceMouthNose, distanceMouthNose, .05) is True and clickRegistered is False ):
				RightClick()
				clickRegistered	= True
			
			else:
				Move( gaze, newGaze )
				clickRegistered	= False
		
		
		
		else:
			# Primary calibration each time face (re)appears
			facePresent		= True
			mouthWidth		= newMouthWidth
			mouseMoveData	= None
			actionTriggered	= False
			clickRegistered	= False








# Determines whether m is significantly greater than n
def GreaterThan( m, n, percentSignificance, referenceValue=1 ):
	difference	= m - n
	
	if( difference <= 0 or difference/referenceValue < percentSignificance ):
		return False
	
	return True



def Pupil( img ):
	bm	= BlobMaker() # create the blob extractor
	# invert the image so the pupil is white, threshold the image, and invert again
	# and then extract the information from the image
	blobs	= bm.extractFromBinary(img.invert().binarize(thresh=240).invert(),img)
	print '0'
	if(len(blobs)>0): # if we got a blob
		print '1'
		blobs[0].draw() # the zeroth blob is the largest blob - draw it
		locationStr	= "("+str(blobs[0].x)+","+str(blobs[0].y)+")"
		# write the blob's centroid to the image
		img.dl().text(locationStr,(0,0),color=Color.RED)
		# save the image
		img.save("images/eye4pupil.jpg")
		# and show us the result.
		img.show()
	
	return blobs[0]



# Mouse functions


def Move( gaze=None, newGaze=None ):
	position	= mouse.position()
	
	if( gaze is None ):
		mouse.move( position[0] + mouseMoveData[0], position[1] + mouseMoveData[1] )
		
		position	= mouse.position()
		if( position[0] <= 0 or position[1] <= 0 or position[0] >= mouseMoveData[2] or position[1] >= mouseMoveData[3] ):
			mouseMoveData	= None
		
	else:
		screenSize	= mouse.screen_size()
		
		shifts		= vector( gaze ) - vector( newGaze ) + 0.0 # x and y shifts as floats
		shifts[1]	= -shifts[1] # Due to coordinate style, both x and y must be inverse; x is already corrected by mirror image
		
		xDistance	= abs( float(position[0] - (0 if shifts[0] < 0 else screenSize[0])) )
		yDistance	= abs( float(position[1] - (0 if shifts[1] < 0 else screenSize[1])) )
		
		TICKS_TO_EDGE	= 10.0 # It will take 10 cycles of the event loop to hit the screen edge, or 1 second (10.0 * 0.1s)
		xMultiplier		= ( xDistance / abs(shifts[0]) ) / TICKS_TO_EDGE
		yMultiplier		= ( yDistance / abs(shifts[1]) ) / TICKS_TO_EDGE
		
		# Multiplier used is the smaller one, because it corresponds with the edge that will be hit first
		shifts	= shifts * (xMultiplier if xMultiplier < yMultiplier else yMultiplier)
		
		# Sets array with data needed to begin and continue mouse movement
		mouseMoveData	= [ shifts[0], shifts[1], screenSize[0] - 1, screenSize[1] - 1 ]
		
		Move()


def LeftClick():
	position	= mouse.position()
	mouse.click( position[0], position[1], 1 )


def RightClick():
	position	= mouse.position()
	mouse.click( position[0], position[1], 3 )


def ScrollUp():
	mouse.scroll( -1 )


def ScrollDown():
	mouse.scroll( 1 )




















































Main()
