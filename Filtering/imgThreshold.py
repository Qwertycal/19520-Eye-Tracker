#author: Nadezhda Shivarova
#date created: 19/03/16
#Description: Combining thresholding and math morphology into
#a single function to use within main()

import numpy as np
import math
import cv2
import removeOutliersThresh as outliers
import bi_level_img_threshold as thresh


from matplotlib import pyplot as plt


def imgThreshold(frame):

    # Convert to greyscale frame
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('original',frame_gray)

    # Create structuring element - disk to remove glint
    struct_el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))
    frame_open = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, struct_el)
    cv2.imshow('open',frame_open)

    # Get histogram of frame
    # more efficient than calcHist and eliminates memory error
    hist_img = np.bincount(frame_gray.flatten())
    print('len_hist',len(hist_img))
    #normalise 
    #hist_img = np.divide(hist_img, float(max(hist_img)))    
    #hist_img = cv2.calcHist([frame], [0], None, [256], [0, 256])
    #plt.plot(hist_img)
    #plt.show()

    # Pass frame to histogram adjustment to remove ouliers - if necessary
    #hist_no_outliers, lower_index = outliers.removeOutliersThresh(hist_img)
    #print('hist_short',len(hist_no_outliers))
    #plt.plot(hist_no_outliers)
    #plt.show()

    # Pass histogram to adaptive thresholding to determine level
    threshLevel = thresh.bi_level_img_threshold(hist_img)

    if(threshLevel > 100):
        threshLevel = 45

    # Adjust start index of hist and add manual level adjustment
    #threshLevelAdjust = threshLevel + lower_index
    #print('Bi level thresh', threshLevelAdjust)


    # Threshold frame using level obtained from adaptive threshold
    ret,threshPupil = cv2.threshold(frame_open,threshLevel,255,cv2.THRESH_BINARY)
    cv2.imshow('thresh pupil',threshPupil)
   

    # Invert and threshold frame to isolate only glint
    #frameInv = np.invert(frame_gray)
    #cv2.imshow('frameInv',frameInv)

    ret,threshGlint = cv2.threshold(frame_gray,200,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh glint',threshGlint)

    return threshPupil, threshGlint