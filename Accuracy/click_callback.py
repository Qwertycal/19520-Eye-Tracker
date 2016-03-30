# import the necessary packages
import argparse
import cv2
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
click_count = 0

def click_callback(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
	global click_count
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:		
		refPt = [(x, y)]
		click_count += 1
		print('L Button down')
		print('X', x)
		print('Y', y)


		
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished	
		refPt = [(x, y)]
		click_count += 1
		print('L Button up')
		print('X', x)
		print('Y', y)
