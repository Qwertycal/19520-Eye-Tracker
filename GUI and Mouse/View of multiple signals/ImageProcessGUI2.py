import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from Tkinter import *
import cv2
from PIL import Image, ImageTk
import pyautogui

import numpy as np
import math
import cv2
import removeOutliersThresh as outliers
import bi_level_img_threshold as thresh
import edgeDetection as edgeDet
import eyeTrackingMainEdited as etMain

width, height = 302, 270
screenwidth, screenheight = pyautogui.size()
cap = cv2.VideoCapture('Eye.mov')
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

print(str(screenwidth) + ', ' + str(screenheight))
root = Tk()
root.title("Testing Mode")
root.bind('<Escape>', lambda e: root.quit())
root.attributes("-fullscreen", True)

#Create Frame
mainFrame = Frame(root)

devViewFrame = Frame(mainFrame, bg = "blue", width = screenwidth, height = 300)
userViewFrame = Frame(mainFrame, bg = "red", width = (screenwidth - 300), height = (screenheight - 300))
coordsFrame = Frame(mainFrame, bg = "black", width = 300, height = (screenheight - 300))
videoFrame1 = Frame(devViewFrame, bg = "green", width = (screenwidth/4), height = height)
videoFrame2 = Frame(devViewFrame, bg = "green", width = (screenwidth/4), height = height)
videoFrame3 = Frame(devViewFrame, bg = "green", width = (screenwidth/4), height = height)
videoFrame4 = Frame(devViewFrame, bg = "green", width = (screenwidth/4), height = height)
buttonFrame = Frame(mainFrame, width = screenwidth)
#desktopViewFrame = Frame(userViewFrame, bg = "red", width = 500, height = 650)

#Create Buttons
mode = IntVar()
devModeB = Radiobutton(buttonFrame,text="Developer Mode",variable=mode,value=1)
userModeB = Radiobutton(buttonFrame,text="User Mode",variable=mode,value=2)
recordB = Button(buttonFrame, text = "Record")
stopB = Button(buttonFrame, text = "Stop")

#for Text width is mesaured in the number of characters, height is the number of lines displayed
outputCoOrds = Text(coordsFrame, width = 42, height = 20)
videoStream1 = Label(videoFrame1)
videoStream2 = Label(videoFrame2)
videoStream3 = Label(videoFrame3)
videoStream4 = Label(videoFrame4)

#Put all of the elements into the GUI
mainFrame.grid(row = 0, column =0, sticky = N)
devViewFrame.grid(row = 1, column = 0, columnspan = 4, rowspan = 2, sticky = N)
userViewFrame.grid(row = 3, column = 3, sticky = N)
coordsFrame.grid(row = 3, column =0, sticky = NW)
videoFrame1.grid(row = 1, column = 0, sticky = W)
videoFrame2.grid(row = 1, column = 1, sticky = W)
videoFrame3.grid(row = 1, column = 2, sticky = W)
videoFrame4.grid(row = 1, column = 3, sticky = W)
buttonFrame.grid(row = 0, column = 0, columnspan = 4,sticky = N)
#userButtonFrame.grid(row = 0, column = 0, sticky = N)
#desktopViewFrame.grid(row = 1, column = 0, sticky = N)

devModeB.grid (row = 0, column =0, sticky = E)
userModeB.grid (row = 0, column = 1, sticky = E)
recordB.grid (row = 0, column = 2, sticky = W)
stopB.grid (row = 0, column = 3, sticky = W)
outputCoOrds.grid(row = 0, column = 0, sticky = NW)
videoStream1.grid()
videoStream2.grid()
videoStream3.grid()
videoStream4.grid()

#Show frame
def show_frame():
    frame_open = etMain.startFrame()
    frame_resized = cv2.resize(frame_open, (width, height), interpolation = cv2.INTER_AREA)
    #cv2.imshow('open',frame_open)
    img = Image.fromarray(frame_resized)
    imgtk = ImageTk.PhotoImage(image=img)
    videoStream1.imgtk = imgtk
    videoStream1.configure(image=imgtk)
    videoStream1.after(30, show_frame)

def show_frame2():
    frameBinary = etMain.thresholdFrame()
    frameB_resized = cv2.resize(frameBinary, (width, height), interpolation = cv2.INTER_AREA)
    img = Image.fromarray(frameB_resized)
    imgtk = ImageTk.PhotoImage(image=img)
    videoStream2.imgtk = imgtk
    videoStream2.configure(image=imgtk)
    videoStream2.after(30, show_frame2)

def show_frame3():
    frame_open = etMain.startFrame()
    frameBinary = etMain.thresholdFrame()
    frameCopy = etMain.detectedFrame()
    frameC_resized = cv2.resize(frameCopy, (width, height), interpolation = cv2.INTER_AREA)
    img = Image.fromarray(frameC_resized)
    imgtk = ImageTk.PhotoImage(image=img)
    videoStream3.imgtk = imgtk
    videoStream3.configure(image=imgtk)
    videoStream3.after(30, show_frame3)

def show_frame4():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image = cv2.resize(cv2image, (width, height));
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    videoStream4.imgtk = imgtk
    videoStream4.configure(image=imgtk)
    videoStream4.after(30, show_frame4)

show_frame()
show_frame2()
show_frame3()
show_frame4()
root.mainloop()