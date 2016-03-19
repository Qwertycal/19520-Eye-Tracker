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

from matplotlib import pyplot as plt


#Solutions obtained from 'Eye.MOV'
aOriginal = [576.217396, -24.047559, 1.0915599, -0.221105357, -0.025469321, 0.037511114]
bOriginal = [995.77047, -1.67122664, 12.67059, 0.018357141, 0.028264854, 0.012302]

def getGazePoint(solutionsA, solutionsB, pupilX, pupilY, glintX, glintY):
    global target
    #	"Returns the user's gaze point"
    
    #Calculate Delta X and Delta Y
    deltaX = pupilX - glintX
    deltaY = pupilY - glintY
    
    #Get X and Y coordinates
    gazeX = solutionsA[0] + (solutionsA[1]*deltaX) + (solutionsA[2]*deltaY) + (solutionsA[3]*deltaX*deltaY) + (solutionsA[4]*(deltaX**2)) + (solutionsA[5]*(deltaY**2))
    
    gazeY = solutionsB[0] + (solutionsB[1]*deltaX) + (solutionsB[2]*deltaY) + (solutionsB[3]*deltaX*deltaY) + (solutionsB[4]*(deltaX**2)) + (solutionsB[5]*(deltaY**2))
    
    #    print "i"
    
    print "%d %d" % (gazeX, gazeY)
    
    #    target = open('gaze_points.txt', 'a')
    #    target.write("%d %d \n" % (gazeX, gazeY))
    #    target.close()
    
    #	print gazeY
    return (gazeX, gazeY);





# Open video capture
cap = cv2.VideoCapture('Eye.mov')
#cap = cv2.VideoCapture('Yousif Eye.mov')
#cap = cv2.VideoCapture('/Users/colinmcnicol/Yousif Eye.mov')
i = 0

while(cap.isOpened()):

    # Read a frame from feed
    ret, frame = cap.read()
    #print frame.shape
    #frame = frame[100:570, 370:1000]
    #print frame_gray.shape

    # Threshold image for pupil and glint separately
    threshPupil, threshGlint = imgThresholdVideo.imgThresholdVideo(frame)
    

    # Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
    print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
    if cpX is None or cpY is None or ccX is None or ccY is None:
        print('pupil or corneal not detected, skipping...')
    elif abs(cpX - ccX) > 40 or abs(cpY - ccY) > 70:
        print('pupil and corneal are too far apart, skipping...')
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
        x, y = getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)


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