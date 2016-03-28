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

screenwidth, screenheight = pyautogui.size()
vidWidth = (screenwidth/2) - 5
vidHeight = (screenheight/2) - 30
cap = cv2.VideoCapture('Eye.mov')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, vidWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vidHeight)

#Solutions obtained from 'Eye.MOV'
aOriginal = [576.217396, -24.047559, 1.0915599, -0.221105357, -0.025469321, 0.037511114]
bOriginal = [995.77047, -1.67122664, 12.67059, 0.018357141, 0.028264854, 0.012302]

print(str(screenwidth) + ', ' + str(screenheight))
root = Tk()
root.title("Testing Mode")
root.bind('<Escape>', lambda e: root.destroy())
root.attributes("-fullscreen", True)

#Create Frame
mainFrame = Frame(root)

devViewFrame = Frame(mainFrame, bg = "green", width = screenwidth, height = screenheight)
videoFrame1 = Frame(devViewFrame, width = vidWidth, height = vidHeight)
videoFrame2 = Frame(devViewFrame, width = vidWidth, height = vidHeight)
videoFrame3 = Frame(devViewFrame, width = vidWidth, height = vidHeight)
videoFrame4 = Frame(devViewFrame, width = vidWidth, height = vidHeight)

#Video Frames
videoStream1 = Label(videoFrame1)
videoStream2 = Label(videoFrame2)
videoStream3 = Label(videoFrame3)
videoStream4 = Label(videoFrame4)

#Put all of the elements into the GUI
mainFrame.grid(row = 0, column =0, sticky = N)
devViewFrame.grid(row = 1, column = 0, columnspan = 4, rowspan = 2, sticky = N)

videoFrame1.grid(row = 1, column = 0, sticky = W)
videoFrame2.grid(row = 1, column = 1, sticky = W)
videoFrame3.grid(row = 2, column = 0, sticky = W)
videoFrame4.grid(row = 2, column = 1, sticky = W)

videoStream1.grid()
videoStream2.grid()
videoStream3.grid()
videoStream4.grid()

#Show frame
def show_frame():
    #while(cap.isOpened()):
    ret, frame = cap.read()
    flipFrame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image, (vidWidth, vidHeight));
    img1 = Image.fromarray(cv2image)
    imgtk1 = ImageTk.PhotoImage(image=img1)
    videoStream1.imgtk1 = imgtk1
    videoStream1.configure(image=imgtk1)
    
    threshPupil, threshGlint = imgThresholdVideo.imgThresholdVideo(frame)
    frame_resized = cv2.resize(threshPupil, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
    frame_resized = cv2.flip(frame_resized, 1)
    img2 = Image.fromarray(frame_resized)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    videoStream2.imgtk2 = imgtk2
    videoStream2.configure(image=imgtk2)

    frameB_resized = cv2.resize(threshGlint, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
    frameB_resized = cv2.flip(frameB_resized, 1)
    img3 = Image.fromarray(frameB_resized)
    imgtk3 = ImageTk.PhotoImage(image=img3)
    videoStream3.imgtk3 = imgtk3
    videoStream3.configure(image=imgtk3)
        
    # Edge Detection of binary frame
    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithmVideo(threshPupil,threshGlint)
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
        
        if(frameCopy != None):
            frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
            frameC_resized = cv2.flip(frameC_resized, 1)
            img4 = Image.fromarray(frameC_resized)
            imgtk4 = ImageTk.PhotoImage(image=img4)
            videoStream4.imgtk4 = imgtk4
            videoStream4.configure(image=imgtk4)

        # Centre points of glint and pupil pass to vector
        x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
    
        # Coordinates on screen
#ATE.move_mouse(x,y)
    
    videoStream1.after(5, show_frame)

show_frame()
root.mainloop()

cap.release()