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
import imgThresholdVideo
import AllTogetherEdit as ATE
import getGazePoint as GGP

from matplotlib import pyplot as plt


#Solutions obtained from 'Eye.MOV'
aOriginal = [576.217396, -24.047559, 1.0915599, -0.221105357, -0.025469321, 0.037511114]
bOriginal = [995.77047, -1.67122664, 12.67059, 0.018357141, 0.028264854, 0.012302]

# Open video capture
#cap = cv2.VideoCapture('Eye.mov')
#cap = cv2.VideoCapture('Yousif Eye.mov')
cap = cv2.VideoCapture('/Users/colinmcnicol/Yousif Eye.mov')
i = 0

while(cap.isOpened()):

    # Read a frame from feed
    ret, frame = cap.read()
    print frame.shape
    frame = frame[100:570, 370:1000]
    #print frame_gray.shape

    # Threshold image for pupil and glint separately
    threshPupil, threshGlint = imgThresholdVideo.imgThresholdVideo(frame)
    

    # Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithmVideo(threshPupil,threshGlint)
    print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
    print successfullyDetected
    if cpX is None or cpY is None or ccX is None or ccY is None:
        print('pupil or corneal not detected, skipping...')
    else:
        print('Delta X: %d  Delta Y: %d' % (abs(cpX - ccX),abs(cpY - ccY)) )
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

        cv2.namedWindow('frame detected',cv2.WINDOW_NORMAL)
        cv2.imshow('frame detected', frameCopy)
        
        # Centre points of glint and pupil pass to vector
        x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)


        # Coordinates on screen
    #        ATE.move_mouse(x,y)



        # Show frames
        #cv2.imshow('frame',frame_gray)
        #cv2.imshow('binary',frameBinary)
        #cv2.imshow('binary inv', frameBinaryInv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()