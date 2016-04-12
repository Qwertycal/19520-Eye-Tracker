#author: Nadezhda Shivarova
#date created: 19/03/16
#Description: Combining thresholding and math morphology into
#a single function to use within main()

import numpy as np
import math
import cv2

from matplotlib import pyplot as plt


def imgThresholdVideo(frame):

   # Convert to greyscale frame
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Get histogram of frame
    #hist_img = cv2.calcHist([frame], [0], None, [256], [0, 256])
    #plt.plot(hist_img)
    #plt.show()
    #cv2.imshow('frame_gray',frame_gray)
    
    #Equalise image to improve constrast - stretch histogram
    frame_eq = cv2.equalizeHist(frame_gray)
    #cv2.imshow('frame_equalized',frame_eq)
    # more efficient than calcHist and eliminates memory error
    hist_img = np.bincount(frame_eq.flatten())
    #hist_img = cv2.calcHist([frame_eq], [0], None, [256], [0, 256])
    # normalise to 1
    hist_img = np.divide(hist_img, float(max(hist_img)))


    # Adjust start index of hist and add manual level adjustment
    # Manually set threshold for video
    threshLevelAdjust = 35

    #Morphological opening to remove glint
    struct_el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(28,28))
    frame_open = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, struct_el)
    #cv2.imshow('open',frame_open)

    # Threshold frame using level set
    ret,threshPupil = cv2.threshold(frame_open,threshLevelAdjust,255,cv2.THRESH_BINARY)
    #cv2.namedWindow('thresh pipil',cv2.WINDOW_NORMAL)
    #cv2.imshow('thresh pupil',threshPupil)

    # Invert and threshold frame to isolate only glint
    frameInv = np.invert(frame_gray)

    ret,threshGlint = cv2.threshold(frameInv,30,255,cv2.THRESH_BINARY_INV)
    #cv2.namedWindow('thresh glint',cv2.WINDOW_NORMAL)
    #cv2.imshow('thresh glint',threshGlint)

    return threshPupil, threshGlint