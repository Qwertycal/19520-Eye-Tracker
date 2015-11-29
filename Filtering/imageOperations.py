import numpy as np
import cv2

from matplotlib import pyplot as plt

#second arg is flag to load as colour, grey or unchanged; 1, 0, -1
img = cv2.imread('Img3.png',cv2.IMREAD_UNCHANGED) #load image as is; then convert to greyscale

#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image', img)

#convert image to greyscale
img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('image_grey', img_grey)

#bilateral filtering to preserve edges
#img_filt = cv2.bilateralFilter(img_grey,15,180,180)


#------ Disadvantage with global thresholding due to the fact that lighting may change due to ambient light interference
#in different rooms etc...
threshVal = 60

# ----- Four different ways to threshold args(img, threshold_val, maxValue -val pixel is set to, type of threshold)
ret,threshBin1 				= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_BINARY)
#ret,threshBinInv2 			= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_BINARY_INV)
#ret,threshThreshTrunc3 		= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_TRUNC)
#ret,threshThreshToZero4    	= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_TOZERO)
#ret,threshThreshToZeroInv5 	= cv2.threshold(img_grey,threshVal,255,cv2.THRESH_TOZERO_INV)

#titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
#images = [img_grey, threshBin1 , threshBinInv2, threshThreshTrunc3, threshThreshToZero4, threshThreshToZeroInv5]

#for i in xrange(6):
#    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#    plt.title(titles[i])
#    plt.xticks([]),plt.yticks([])

#plt.show()

#----- Alternative global threshold - mask the image to preserve only the middle where the eye is.
#----- Use a histogram and use the median as a threshold value and apply this value globally.

#create a mask 400x300 => 23% of the image
mask_len 	= 400
mask_width = 300 
mask = np.zeros(img_grey.shape[:2], np.uint8)
mask[313-(mask_width/2):313+(mask_width/2), 417-(mask_len/2):417+(mask_len/2)] = 255
masked_img = cv2.bitwise_or(img_grey,img_grey, mask = mask)
cv2.imshow('masked', masked_img)
cv2.imshow('mask', mask)

#Cut out only the masked section of the image and find out the lowest pixel value
masked_img_cut = masked_img[313-(mask_width/2):313+(mask_width/2), 417-(mask_len/2):417+(mask_len/2)]
cv2.imshow('masked_cut', masked_img_cut)
hist_full = cv2.calcHist([masked_img_cut],[0],None,[256],[0,256])
print(hist_full)
plt.plot(hist_full)
plt.xlabel('Pixel Intensity')
plt.ylabel('Number of Pixels')
#plt.savefig('Img1_MaskHistogram.png')
#plt.show()
threshValMask = np.amin(hist_full)
print('Min hist',threshValMask)
print('Max hist',np.amax(masked_img_cut))

#find optimal thresholding value using Otsu's thresholding on the masked cut image
retOtsu,threshMask  = cv2.threshold(masked_img_cut,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print(retOtsu)
ret,threshBinMask   = cv2.threshold(img_grey,retOtsu,255,cv2.THRESH_BINARY)
cv2.imshow('Binary with mask',threshBinMask)


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

plt.savefig('Img3_Thresholding methods.png')
#plt.show()

#cv2.waitKey(0) #keyboard binding function; arg- time in ms; 0 indicates indefinite wait for any key
#cv2.destroyAllWindows()
