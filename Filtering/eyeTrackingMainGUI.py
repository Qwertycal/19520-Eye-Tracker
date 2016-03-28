#author: Rachel Hutchinson
#date created: 28th March
#description: shows the original feed, and has two buttons, one with the option to
#recalibrate the system, and the other with the option to quit
#this includes the code from the original main calls other mehtods from their seperate scripts

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from Tkinter import *
from PIL import Image, ImageTk
import pyautogui

import numpy as np
import math
import cv2
import removeOutliersThresh as outliers
import bi_level_img_threshold as thresh
import edgeDetection as edgeDet
import AllTogetherEdit as ATE
import getGazePoint as GGP
import imgThreshold
import getCalibrationUnknowns as GCU

#Find the screen width & set the approprite size for the feed
screenwidth, screenheight = pyautogui.size()
vidWidth = (screenwidth/4)
vidHeight = (screenheight/4)

#Capture the feed coming from the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, vidWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vidHeight)

#Calibration values
pupilX = [275, 264, 244, 280, 261, 239, 277, 259, 240]
pupilY = [178, 178, 178, 183, 183, 182, 188, 188, 190]
glintX = [278, 273, 264, 281, 272, 262, 279, 270, 259]
glintY = [190, 188, 190, 191, 189, 190, 190, 191, 192]
calibrationX = [213, 639, 1065, 213, 639, 1065, 213, 639, 1065]
calibrationY = [133, 133, 133, 399, 399, 399, 665, 665, 665]

aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY, calibrationX, calibrationY)

#Set up how big the gui window should be, and where it should be positioned on screen
#Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
w = vidWidth + 4
h = vidHeight + 34
x = screenwidth - (w + 10)
y = screenheight - (h + 60)

#Set up the GUI
root = Tk()
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title("Eye Tracking")
root.bind('<Escape>', lambda e: root.destroy())

#Set up the commands to be called on the button presses
def recalibrate():
    print ('Recalibrate')

def quit():
    print ('Quit')
    root.destroy()

#Create button frame
buttonFrame = Frame(root)

#Create label for video to go in
videoStream1 = Label(root)

#Create buttons
recalibrateButton = Button(buttonFrame, text = "Recalibrate", command = recalibrate)
quitButton = Button(buttonFrame, text = "Quit", command = quit)

#Put all of the elements into the GUI
buttonFrame.grid(row = 1, column = 0, sticky = N)

videoStream1.grid(row = 0, column = 0)
recalibrateButton.grid(row = 0, column = 0)
quitButton.grid(row = 0, column = 1)

#Show frame
def show_frame():
    #Read the input feed, flip it, resize it and show it in the corresponding label
    #Original, flipped feed
    ret, frame = cap.read()
    flipFrame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image, (vidWidth, vidHeight));
    img1 = Image.fromarray(cv2image)
    imgtk1 = ImageTk.PhotoImage(image=img1)
    videoStream1.imgtk1 = imgtk1
    videoStream1.configure(image=imgtk1)

    #Call the threholding function
    threshPupil, threshGlint = imgThreshold.imgThreshold(frame)

    #Call Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
    #Implement functionality that was used in main to draw around the pupil and glint
    print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
    print successfullyDetected
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
        
        #Code that will hopefully show the detected pupil, if uncommented
#        if(frameCopy != None):
#            frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
#            frameC_resized = cv2.flip(frameC_resized, 1)
#            img1 = Image.fromarray(frameC_resized)
#            imgtk1 = ImageTk.PhotoImage(image=img1)
#            videoStream1.imgtk1 = imgtk1
#            videoStream1.configure(image=imgtk1)

        # Centre points of glint and pupil pass to vector
        x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
    
        # Coordinates on screen
        #ATE.move_mouse(x,y)
    
    videoStream1.after(5, show_frame)

show_frame()
root.mainloop()

cap.release()