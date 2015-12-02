import numpy as np
import math
import cv2
import removeOutliersThresh
import bi_level_img_threshold

from matplotlib import pyplot as plt

#second arg is flag to load as colour, grey or unchanged; 1, 0, -1
img = cv2.imread('Img3.png',cv2.IMREAD_UNCHANGED) #load image as is; then convert to greyscale

#convert image to greyscale
img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#------ Disadvantage with global thresholding due to the fact that lighting may change due to ambient light interference
#in different rooms etc...
threshVal = 60

# ----- Four different ways to threshold args(img, threshold_val, maxValue -val pixel is set to, type of threshold)
ret,threshBin1 	= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_BINARY)

#----- Alternative global threshold - mask the image to preserve only the middle where the eye is.
#----- Use a histogram and use the median as a threshold value and apply this value globally.

#create a mask image block 400x300 => 23% of the image
mask_len 	= 400
mask_width  = 300 

#Cut out only the masked section of the image and find out the lowest pixel value
img_cut = img_grey[313-(mask_width/2):313+(mask_width/2), 417-(mask_len/2):417+(mask_len/2)]
#cv2.imshow('masked_cut', img_cut)

#will need lower index to add onto the threshold because the histogram was moved forward
hist_img_cut = cv2.calcHist([img_cut], [0], None, [256], [0, 256])
# plt.subplot(2, 1, 1)
# plt.plot(hist_img_cut)
# plt.xlabel('Pixel value')
# plt.ylabel('No. of pixels')
# plt.title('Histogram Image cut')

#remove outliers past the upper bound of the interquartile range
#img_cut_no_outliers, upper_bound = removeOutliers.removeOutliers(img_cut)

#remove outliers using threshold
hist_img_cut_no_outliers, lower_index = removeOutliersThresh.removeOutliersThresh(hist_img_cut)
hist_x_values = range(lower_index,len(hist_img_cut_no_outliers) + lower_index)
print('len hist_img_cut_no_outliers ', len(hist_img_cut_no_outliers), 'ind_low', lower_index, 'y ', len(hist_x_values))

# plt.subplot(2, 1, 2)
# plt.plot(hist_x_values, hist_img_cut_no_outliers)
# plt.xlabel('Pixel value')
# plt.ylabel('No. of pixels')
#plt.savefig('Img_3_Histogram_outliers_Thresholding.png')


#find the threshold using bi level img thresholding
threshBalanced = bi_level_img_threshold.bi_level_img_threshold(hist_img_cut_no_outliers)
threshAdap = threshBalanced + lower_index - 15
print('Bi level thresh', threshAdap)


ret,threshBin1 	= cv2.threshold(img_grey,threshAdap,255,cv2.THRESH_BINARY)

plt.subplot(2, 1, 1)
plt.imshow(img_grey,'gray')
plt.title('Original')
plt.subplot(2, 1, 2)
plt.imshow(threshBin1,'gray')
plt.title('Balanced Histogram Threshold = '+ str(threshAdap))
#plt.savefig('Img3_ThreshAdapBalanced.png')
plt.show()





#plt.show()
#find optimal thresholding value using Otsu's thresholding on the masked cut image
retOtsu,threshMask  = cv2.threshold(img_cut,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#print('Otsu',retOtsu)
ret,threshBinMask   = cv2.threshold(img_grey,retOtsu,255,cv2.THRESH_BINARY)
#cv2.imshow('Binary with mask',threshBinMask)


#----- Better approach is to use adaptive thresholding which decide locally on a threshold for a neightbour of images

threshAdapMean 		= cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 5)
threshAdapGaussian 	= cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 5)

titles = ['Img3_OriginalImage', 'Img3_GlobalThresholding(v=' + str(threshVal) +')',
            'Img3_AdaptiveMeanThresholding', 'Img3_Adaptive Gaussian Thresholding']
images = [img_grey, threshBin1, threshAdapMean, threshAdapGaussian]

for i in xrange(4):
	plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])

#plt.savefig('Img3_Thresholding methods.png')
#plt.show()

#cv2.waitKey(0) #keyboard binding function; arg- time in ms; 0 indicates indefinite wait for any key
#cv2.destroyAllWindows()
