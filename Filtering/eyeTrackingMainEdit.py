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
#import AllTogetherEdit as ATE
#import getGazePoint as GGP
import imgThreshold

from matplotlib import pyplot as plt

#Solutions obtained from 'Eye.MOV'
aOriginal = [402.84482, -20.6854858, -7.40409644, -0.139460511, 
-0.0316878766, -0.0595331782]
bOriginal = [496.58251, 16.006643, 8.2113024, 0.2931556,
0.27153592, 0.075294837]


# Open video capture
cap = cv2.VideoCapture(1)
i = 0
print(cap)
print(cap.isOpened())

while(cap.isOpened()):

    # Read a frame from feed
    ret, frame = cap.read()
    
    threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
    
    # Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc = edgeDet.edgeDetectionAlgorithm(threshPupil, threshGlint)
#    print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
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

        print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
        # Centre points of glint and pupil pass to vector
#        print('Gaze points X and Y:')
        #x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
        
        #ATE.move_mouse(x,y)
	
        # Show frames
        #cv2.imshow('frame',frame_gray)
#        cv2.imshow('binary',frameBinary)
        #cv2.imshow('binary inv', frameBinaryInv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#target.close()
cv2.destroyAllWindows()