
import numpy as np
import cv2
from matplotlib import pyplot as plt


def thresholding(img, threshValue):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (T, thresh) = cv2.threshold(gray, threshValue, 255, cv2.THRESH_BINARY_INV) # if pixel value is > 10 change to white 255
    
    return thresh



def getContours(image):
    global mask
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    
    mainContour = None
    mainMoments = None
    contourCentreX = None
    contourCentreY = None
    
    maxArea = 0.0
#    print " "
    for c in cnts:
        area = cv2.contourArea(c)
#        print area
        if area > maxArea and area < 47000: #ensure the correct contour is detected 15000
            maxArea = area
            mainContour = c
            M = cv2.moments(c)
            contourCentreX = int(M['m10']/M['m00'])
            contourCentreY = int(M['m01']/M['m00'])

#    if mainContour is None:
#        print "pupil contour is none"

    return contourCentreX, contourCentreY, mainContour



#input is 2 thresholded images. 1.for pupil 2. for corneal
def edgeDetectionAlgorithm(pupilThreshold, cornealThreshold):
    global isPupilDetected
    global isCornealDetected

    cpX = None
    cpY = None
    ccX = None
    ccY = None
    cp = None
    cc = None
    
    isPupilDetected = 0
    isCornealDetected = 0


    #--------------------- Detect pupil -----------------#
    cpX, cpY, cp = getContours(pupilThreshold)
    
    
    if cpX is None or cpY is None:  #check is pupil has been detected
        isPupilDetected = 1
        print " pupil not detected"
        cv2.waitKey(1)

    else:
        #--------------------- Detect corneal -----------------#
        
        # Need thresholded image for corneal detection
        ccX, ccY, cc = getContours(cornealThreshold)
#        print "corneal values"
#        print ccX
#        print ccY


        if ccX is None or ccY is None:  #check is pupil has been detected
            isCornealDetected = 1
            print "corneal not detected"
            cv2.waitKey(1)

    return cpX,cpY,cp,ccX,ccY,cc



def main():
    global frame
    global isPupilDetected
    global isCornealDetected
    
    isPupilDetected = 0
    isCornealDetected = 0
    
    cap = cv2.VideoCapture('/Users/colinmcnicol/Documents/David/CES/Group Project/HeatherSampleData/Eye.mov')
    
#    while(isPupilDetected == 0 and isCornealDetected == 0):
    while(1):
        ret, frame = cap.read()

    #    cv2.imshow('video', frameVideo)
    #    frame = cv2.imread('/Users/colinmcnicol/Pictures/eyeGlint1.png')
        threshPupil = thresholding(frame, 35)

        invertFrame = np.invert(frame)
        threshCorneal = thresholding(invertFrame,15)
        
        
        cpX,cpY,cp,ccX,ccY,cc = edgeDetectionAlgorithm(threshPupil,threshCorneal)
        if isPupilDetected or isCornealDetected == 1:
            print "pupil or corneal not detected"
        else:
        
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
            cv2.waitKey(1)

    if cv2.waitKey(0) == 27:
        print "escape pressed"
        cv2.destroyAllWindows()



if __name__ == "__main__":
    main()





