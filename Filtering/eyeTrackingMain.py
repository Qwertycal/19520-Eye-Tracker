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
import edgeDetection as edgeDet

from matplotlib import pyplot as plt

# Open video capture
cap = cv2.VideoCapture('Eye.mov')
i = 0
	
while(cap.isOpened()):

    # Read a frame from feed
    ret, frame = cap.read()
    # Convert to greyscale frame
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    i = i+1
    print('i ', i)
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
    threshLevelAdjust = threshLevel + lower_index + 15
    #print('Bi level thresh', threshLevelAdjust)

    struct_el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
    frame_open = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, struct_el)
    cv2.imshow('open',frame_open)
    # Threshold frame using level obtained from adaptive threshold
    ret,frameBinary = cv2.threshold(frame_open,threshLevelAdjust,255,cv2.THRESH_BINARY)
    cv2.imshow('binaryOrig',frameBinary)

    # Invert and threshold frame to isolate only glint
    frameInv = np.invert(frame_gray)

    ret,frameBinaryInv = cv2.threshold(frameInv,30,255,cv2.THRESH_BINARY_INV)
    
    # Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc = edgeDet.edgeDetectionAlgorithm(frameBinary,frameBinaryInv)
    print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
    if cpX is None or cpY is None or ccX is None or ccY is None:
        print('pupil or corneal not detected, skipping...')
    else:   
        # Ellipse Fitting
        frameCopy = frame.copy()
    
        #draw pupil centre
        cv2.circle(frameCopy, (cpX,cpY),3,(0,255,0),-1)
        
        #draw pupil circumference
        cv2.drawContours(frameCopy,cp,-1,(0,0,255),3)
    
        #draw corneal centre
        cv2.circle(frameCopy, (ccX,ccY),3,(0,255,0),-1)
    
        #draw corneal circumference
        cv2.drawContours(frameCopy,cc,-1,(0,0,255),3)
    
        cv2.imshow('frame detected', frameCopy)
        # Centre points of glint and pupil pass to vector


        # Coordinates on screen




        # Show frames
        #cv2.imshow('frame',frame_gray)
        cv2.imshow('binary',frameBinary)
        #cv2.imshow('binary inv', frameBinaryInv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
