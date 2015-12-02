#author: Nadezhda Shivarova
#date created: 1/12/15
#Description: Calculate the upper bound/lower of the interquartile range to identify outliers 
# i.e. remove pixel values close to 255

import numpy as np
import math

def removeOutliersIQR(img):

	qs = np.percentile(img, [25, 75])
	iqr = qs[1] - qs[0]
	#lower_bound = math.floor(qs[0] - 1.5 * iqr)
	upper_bound = math.ceil(1.5 * iqr + qs[1])
	#print('Lower bound ', lower_bound)
	print('Upper bound ', upper_bound)

	#remove the outliers from the array
	img_no_outliers = []
	for x in img.flatten():
		if x <= upper_bound:
			img_no_outliers += [x]
	print('func out', len(img_no_outliers))

	return img_no_outliers, upper_bound