#author: Nadezhda Shivarova
#date created: 1/12/15
#Description: Remove outliers in the histogram of the cut out image
#using a threshold 5% of the tallest peak
#scan start of hist until the threshold is reached
#scan end of histogram until thresh is reached
#discard values from ends that are below the threshold

import numpy as np

def removeOutliersThresh(hist):
	#cv2.hist returns a 2D array - make 1D array
	hist = hist.flatten()
	print('Len hist ', len(hist))
	maxpeak = np.amax(hist)
	print('Max', maxpeak)

	#calculate threshold as 5% of maxpeak
	threshold = (maxpeak/100)*5
	print('thresh', threshold)

	#scan histogram from left to right i.e. start to thresh
	lower_index = 0
	for i, x in enumerate(hist):
		if x >= threshold:
			lower_index = i
			break

	upper_index = 0
	for i, x in enumerate(reversed(hist)):
		if x >= threshold:
			upper_index = len(hist)-1 - i
			break

	hist_img_cut_no_outliers = hist[lower_index:upper_index]

	return hist_img_cut_no_outliers, lower_index