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
    # truncate histogram to remove bin 0 and bin 255 instead of removing outliers which
    # removes all the bins
    hist_img = hist_img[1:len(hist_img)-2]

    # Pass histogram to adaptive thresholding to determine level

    threshLevel = thresh.bi_level_img_threshold(hist_img)

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