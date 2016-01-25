# author: Nadezhda Shivarova, Calum Whytock, David McNicol
# date created: 25/01/16
# Description: Amalgamation (main()) of functions for eye tracking. Uploads
# the IR video and thresholds image, identifies pupil and glint
# centre and calculates the direction vector. Each operation is
# organised as a standalone function.
#

import numpy as np
import math
import cv2
import removeOutliersThresh as outliers
import bi_level_img_threshold as thresh

from matplotlib import pyplot as plt

# Open video capture
cap = cv2.VideoCapture('eye.mov')
	
while(cap.isOpened()):
	# Read a frame from feed
	ret, frame = cap.read()
	# Convert to greyscale frame
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Get histogram of frame
	hist_img = cv2.calcHist([frame], [0], None, [256], [0, 256])
	#plt.plot(hist_img)
	#plt.show()

	# Pass frame to histogram adjustment to remove ouliers
	hist_no_outliers, lower_index = outliers.removeOutliersThresh(hist_img)
	#plt.plot(hist_no_outliers)
	#plt.show()

	# Pass histogram to adaptive thresholding to determine level
	threshLevel = thresh.bi_level_img_threshold(hist_no_outliers)

	# Adjust start index of hist and add manual level adjustment
	threshLevelAdjust = threshLevel + lower_index + 25
	print('Bi level thresh', threshLevelAdjust)

	# Threshold frame using level obtained from adaptive threshold
	ret,frameBinary = cv2.threshold(frame,threshLevelAdjust,255,cv2.THRESH_BINARY)


	# Edge Detection of binary frame


	# Ellipse Fitting


	# Centre points of glint and pupil pass to vector


	# Coordinates on screen



	
	# Show frames
	cv2.imshow('frame',frame_gray)
	cv2.imshow('binary',frameBinary)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
