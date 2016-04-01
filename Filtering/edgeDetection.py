
import numpy as np
import cv2
from matplotlib import pyplot as plt


def getContours(image):
    global mask
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    
    maxArea = 0.0
#    print " "
    for c in cnts:
        area = cv2.contourArea(c)
#        print "pupil area: %d" % area
        if area > maxArea and area > 600 and area < 5000: #ensure the correct contour is detected
            M_2 = cv2.moments(c)
            cX = int(M_2['m10']/M_2['m00'])
            cY = int(M_2['m01']/M_2['m00'])
            if cX >= topLeftCornerX and cY >= topLeftCornerY and cX <= bottomRightCornerX and cY <= bottomRightCornerY:
                maxArea = area
                mainContour = c
                M = cv2.moments(c)
                contourCentreX = int(M['m10']/M['m00'])
                contourCentreY = int(M['m01']/M['m00'])

#    if mainContour is None:
#        print "pupil contour is none"

    print maxArea
    return contourCentreX, contourCentreY, mainContour

def getContoursVideo(image):
    global mask
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    
    maxArea = 0.0
    #    print " "
    for c in cnts:
        area = cv2.contourArea(c)
        #        print "pupil area: %d" % area
        if area > maxArea and area > 600 and area < 12000: #ensure the correct contour is detected
            M_2 = cv2.moments(c)
            cX = int(M_2['m10']/M_2['m00'])
            cY = int(M_2['m01']/M_2['m00'])
            if cX >= topLeftCornerX and cY >= topLeftCornerY and cX <= bottomRightCornerX and cY <= bottomRightCornerY:
                maxArea = area
                mainContour = c
                M = cv2.moments(c)
                contourCentreX = int(M['m10']/M['m00'])
                contourCentreY = int(M['m01']/M['m00'])

#    if mainContour is None:
#        print "pupil contour is none"

#    print maxArea
    return contourCentreX, contourCentreY, mainContour


def getContoursCorneal(image):
    global mask
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:len(contours)]
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    contourList = []
    
    maxArea = 0.0
    prevDist = 1000.0
    #    print " "
    for c in cnts:
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        
        if M['m00'] == 0:
            M['m00'] = 1
        
        cX = int(M['m10']/M['m00'])
        cY = int(M['m01']/M['m00'])
        
        if area > maxArea and area < 250 and abs(cpX - cX) < 50 and abs(cpY - cY) < 50 and cY >= cpY: #ensure the correct contour is detected 15000
            deltaX = abs(cpX - cX)
            deltaY = abs(cpY - cY)
            
            dist = np.sqrt(deltaX^2 + deltaY^2)
            if dist < prevDist:
                prevDist = dist
                contourList.append(c)
                maxArea = area
                mainContour = c
                M = cv2.moments(c)
                contourCentreX = int(M['m10']/M['m00'])
                contourCentreY = int(M['m01']/M['m00'])

    contourImg = np.zeros((470,620),np.uint8)
    contourImg = cv2.cvtColor(contourImg, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourImg,contourList,-1,(0,0,255),3)
#cv2.imshow('contourImg',contourImg)

    return contourCentreX, contourCentreY, mainContour


def getContoursCornealVideo(image):
    global mask
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:len(contours)]
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    contourList = []
    
    maxArea = 0.0
    #    print " "
    for c in cnts:
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        
        if M['m00'] == 0:
            M['m00'] = 1
        
        cX = int(M['m10']/M['m00'])
        cY = int(M['m01']/M['m00'])
        
        if area > maxArea and area < 150 and abs(cpX - cX) < 100 and abs(cpY - cY) < 100 : #ensure the correct contour is detected 15000
            contourList.append(c)
            maxArea = area
            mainContour = c
            M = cv2.moments(c)
            contourCentreX = int(M['m10']/M['m00'])
            contourCentreY = int(M['m01']/M['m00'])

    contourImg = np.zeros((470,620),np.uint8)
    contourImg = cv2.cvtColor(contourImg, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourImg,contourList,-1,(0,0,255),3)
#cv2.imshow('contourImg',contourImg)
    
    return contourCentreX, contourCentreY, mainContour



#input is 2 thresholded images. 1.for pupil 2. for corneal
def edgeDetectionAlgorithm(pupilThreshold, cornealThreshold):
    global isPupilDetected
    global isCornealDetected
    global cpX
    global cpY
    global topLeftCornerX
    global topLeftCornerY
    global bottomRightCornerX
    global bottomRightCornerY


    cpX = None
    cpY = None
    ccX = None
    ccY = None
    cp = None
    cc = None
    
    isPupilDetected = 0
    isCornealDetected = 0
    successfullyDetected = True
    
    edgeLimit = 4
    
    w,h = pupilThreshold.shape
    
    topLeftCornerX = h / edgeLimit
    topLeftCornerY = w / edgeLimit
    bottomRightCornerX = h / edgeLimit * (edgeLimit-1)
    bottomRightCornerY = w / edgeLimit * (edgeLimit-1)


    #--------------------- Detect pupil -----------------#
    cpX, cpY, cp = getContours(pupilThreshold)
    

    if cpX is None or cpY is None:  #check is pupil has been detected
        successfullyDetected = False
        print "pupil not detected"
        cv2.waitKey(1)
    else:
        #--------------------- Detect corneal -----------------#
        
        # Need thresholded image for corneal detection
        ccX, ccY, cc = getContoursCorneal(cornealThreshold)
#        print "corneal values"
#        print ccX
#        print ccY


        if ccX is None or ccY is None:  #check is pupil has been detected
            successfullyDetected = False
            print "corneal not detected"
            cv2.waitKey(1)

    return cpX,cpY,cp,ccX,ccY,cc,successfullyDetected


#input is 2 thresholded images. 1.for pupil 2. for corneal
def edgeDetectionAlgorithmVideo(pupilThreshold, cornealThreshold):
    global isPupilDetected
    global isCornealDetected
    global cpX
    global cpY
    global topLeftCornerX
    global topLeftCornerY
    global bottomRightCornerX
    global bottomRightCornerY
    
    
    cpX = None
    cpY = None
    ccX = None
    ccY = None
    cp = None
    cc = None
    
    isPupilDetected = 0
    isCornealDetected = 0
    successfullyDetected = True
    
    edgeLimit =8
    
    w,h = pupilThreshold.shape
    
    topLeftCornerX = h / edgeLimit
    topLeftCornerY = w / edgeLimit
    bottomRightCornerX = h / edgeLimit * (edgeLimit-1)
    bottomRightCornerY = w / edgeLimit * (edgeLimit-1)
    
    
    #--------------------- Detect pupil -----------------#
    cpX, cpY, cp = getContoursVideo(pupilThreshold)
    
    
    if cpX is None or cpY is None:  #check if pupil has been detected
        successfullyDetected = False
        print "pupil not detected"
        cv2.waitKey(1)
    else:
        #--------------------- Detect corneal -----------------#
        
        # Need thresholded image for corneal detection
        ccX, ccY, cc = getContoursCornealVideo(cornealThreshold)
        #        print "corneal values"
        #        print ccX
        #        print ccY
        
        
        if ccX is None or ccY is None:  #check if glint has been detected
            successfullyDetected = False
            print "corneal not detected"
            cv2.waitKey(1)

    return cpX,cpY,cp,ccX,ccY,cc,successfullyDetected

