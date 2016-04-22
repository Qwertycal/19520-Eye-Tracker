
import numpy as np
import cv2
from matplotlib import pyplot as plt

# This function looks for contours (consecutive points) that could potentially be the pupil and narrows contours by area size and location within the frame
def getContours(image):
    global mask
    
    # uses opencv function findContours to find contours
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    
    maxArea = 0.0
    
    # loops through all contours detected and narrows possible pupil by area size and location
    for c in cnts:
        area = cv2.contourArea(c)
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

    return contourCentreX, contourCentreY, mainContour


# This function looks for contours (consecutive points) that could potentially be the pupil and narrows contours by area size and location within the frame. Copy method by used for separate video
def getContoursVideo(image):
    global mask
    _,contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    
    maxArea = 0.0
    
    # loops through all contours detected and narrows possible pupil by area size and location
    for c in cnts:
        area = cv2.contourArea(c)
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

    return contourCentreX, contourCentreY, mainContour

# This function looks for contours (consecutive points) that could potentially be the glint and narrows contours by area size and location to pupil.
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

    return contourCentreX, contourCentreY, mainContour

# This function looks for contours (consecutive points) that could potentially be the glint and narrows contours by area size and location from pupil. Copy method by used for separate video
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

    return contourCentreX, contourCentreY, mainContour



# input is 2 thresholded images. 1.for pupil 2. for corneal. This function sets the boundaries to search for pupil and performs both findContours functions for pupil and glint
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


    #--------------------- Detect pupil ----------------------------------#
    cpX, cpY, cp = getContours(pupilThreshold)
    

    if cpX is None or cpY is None:  #check is pupil has been detected
        successfullyDetected = False
        cv2.waitKey(1)
    else:
    #--------------------- Detect corneal --------------------------------#
        
        # Need thresholded image for corneal detection
        ccX, ccY, cc = getContoursCorneal(cornealThreshold)

        if ccX is None or ccY is None:  #check is pupil has been detected
            successfullyDetected = False
            cv2.waitKey(1)

    return cpX,cpY,cp,ccX,ccY,cc,successfullyDetected


# input is 2 thresholded images. 1.for pupil 2. for corneal. This function sets the boundaries to search for pupil and performs both findContours functions for pupil and glint. This is copy specific for video
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
    
    #------------ Sets boundary for detecting pupil -----------------#
    w,h = pupilThreshold.shape
    
    topLeftCornerX = h / edgeLimit
    topLeftCornerY = w / edgeLimit
    bottomRightCornerX = h / edgeLimit * (edgeLimit-1)
    bottomRightCornerY = w / edgeLimit * (edgeLimit-1)
    
    
    #--------------------- Detect pupil ------------------------------#
    cpX, cpY, cp = getContoursVideo(pupilThreshold)
    
    
    if cpX is None or cpY is None:  #check if pupil has been detected
        successfullyDetected = False
        print "pupil not detected"
        cv2.waitKey(1)
    else:
    #--------------------- Detect corneal ----------------------------#
        
        # Need thresholded image for corneal detection
        ccX, ccY, cc = getContoursCornealVideo(cornealThreshold)
        
        if ccX is None or ccY is None:  #check if glint has been detected
            successfullyDetected = False
            print "corneal not detected"
            cv2.waitKey(1)

    return cpX,cpY,cp,ccX,ccY,cc,successfullyDetected

