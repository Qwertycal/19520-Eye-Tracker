#author: Nadezhda Shivarova
#date created: 30/11/15
#Description: Perform Bi-Level Image Threshold on a histogram to determine the optimal threshold level
#Using the algorithm in the paper Bi Level Img Thresholding, Antonio dos Anjos

import numpy as np

def bi_level_img_threshold( hist ):
   	hist = hist.flatten()
	print('len hist ', len(hist))
	#start and end index of the histogram
	I_s = 0
	I_e = len(hist)-1
	#print('I_e ', I_e, 'I_m ', (I_s+I_e)/2)
	#print('hist [Ie]', hist[I_e])
	# starting point: get right and left weights of histogram and
	# determine the midpoint base triangle

	I_m = (I_s+I_e)/2
	W_l = np.sum(hist[I_s : I_m])  
	W_r = np.sum(hist[I_m+1 : I_e])
	#print('W_l ', W_l, 'W_r ', W_r)

	while (I_s != I_e):
		if (W_r > W_l):
			W_r = W_r - hist[I_e]
			#print('Wr ', W_r)
			I_e = I_e - 1
			#print('Ie new', I_e)

			if ((I_s+I_e)/2 < I_m):
				W_l = W_l - hist[I_m]
				W_r = W_r + hist[I_m]
				I_m = I_m - 1

		#apply the algorithm mirrored, I_m tends towards depression		
		elif (W_l >= W_r):
			W_l = W_l + hist[I_s]
			I_s = I_s + 1

			if ((I_s+I_e)/2 > I_m):
				W_l = W_l + hist[I_m+1]
				W_r = W_r - hist[I_m+1]
				I_m = I_m + 1

	#I_s and I_e get closer until they are equal to I_m
	#I_m is the optimal threshold i.e. depression between left and right side
	return I_m