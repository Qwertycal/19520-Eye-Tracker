#author: Rachel Hutchinson
#date created: 28th March
#description: shows 4 stages in the eye tracking
#process, and includes the code from the original main
#calls other mehtods from their seperate scripts

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
import imgThresholdVideo
import AllTogetherEdit as ATE
import getGazePoint as GGP

#Find the screen width & set the approprite size for each feed
screenwidth, screenheight = pyautogui.size()
vidWidth = (screenwidth/2) - 5
vidHeight = (screenheight/2) - 30

#Open the video file & set it's width
global cap
cap = cv2.VideoCapture('Eye.mov')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, vidWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vidHeight)
global frame_counter
frame_counter = 0

#Solutions obtained from 'Eye.MOV'
aOriginal = [576.217396, -24.047559, 1.0915599, -0.221105357, -0.025469321, 0.037511114]
bOriginal = [995.77047, -1.67122664, 12.67059, 0.018357141, 0.028264854, 0.012302]

def closeWindow():
    print ('Quit')
    lambda e: root.destroy()

#Set up the GUI
root = Tk()
root.title("Demo Mode")
root.bind('<Escape>', lambda e: root.destroy())
root.protocol("WM_DELETE_WINDOW", closeWindow)
root.attributes("-fullscreen", True)

#Create labels for each video feed to go in
videoStream1 = Label(root)
videoStream2 = Label(root)
videoStream3 = Label(root)
videoStream4 = Label(root)

#Put all of the elements into the GUI
videoStream1.grid(row = 0, column = 0)
videoStream2.grid(row = 0, column = 1)
videoStream3.grid(row = 1, column = 0)
videoStream4.grid(row = 1, column = 1)

#Show frame
def show_frame():
    global frame_counter
    global cap
    if frame_counter >= (cap.get(cv2.CAP_PROP_FRAME_COUNT)-5):
        print 'loop condition'
        frame_counter = 0 #Or whatever as long as it is the same as next line
        cap = cv2.VideoCapture('Eye.MOV')
    #Read the input feed, flip it, resize it and show it in the corresponding label
    #Original, flipped feed
    ret, frame = cap.read()
    frame_counter += 1
    flipFrame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight));
    img1 = Image.fromarray(cv2image)
    imgtk1 = ImageTk.PhotoImage(image=img1)
    videoStream1.imgtk1 = imgtk1
    videoStream1.configure(image=imgtk1)
    
    #Call the threholding function (suited for the video feed)
    threshPupil, threshGlint = imgThresholdVideo.imgThresholdVideo(frame)
    #Show the thresholded pupil, same method as above
    frame_resized = cv2.resize(threshPupil, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
    frame_resized = cv2.flip(frame_resized, 1)
    img2 = Image.fromarray(frame_resized)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    videoStream2.imgtk2 = imgtk2
    videoStream2.configure(image=imgtk2)

    #Show the thresholded glint, same method as above
    frameB_resized = cv2.resize(threshGlint, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
    frameB_resized = cv2.flip(frameB_resized, 1)
    img3 = Image.fromarray(frameB_resized)
    imgtk3 = ImageTk.PhotoImage(image=img3)
    videoStream3.imgtk3 = imgtk3
    videoStream3.configure(image=imgtk3)
    
    # Call the edge detection of binary frame (suited for the video feed)
    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithmVideo(threshPupil,threshGlint)
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
        
        #If there is a frame to show, show it.
        if(frameCopy != None):
            frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
            frameC_resized = cv2.flip(frameC_resized, 1)
            img4 = Image.fromarray(frameC_resized)
            imgtk4 = ImageTk.PhotoImage(image=img4)
            videoStream4.imgtk4 = imgtk4
            videoStream4.configure(image=imgtk4)

        # Centre points of glint and pupil pass to vector
        x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
    
        # Move to coordinates on screen
        #ATE.move_mouse(x,y)
    
    videoStream1.after(5, show_frame)

show_frame()
root.mainloop()

cap.release()