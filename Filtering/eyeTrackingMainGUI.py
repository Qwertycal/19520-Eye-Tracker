#author: Rachel Hutchinson
#date created: 28th March
#description: shows the original feed, and has two buttons, one with the option to
#recalibrate the system, and the other with the option to quit
#this includes the code from the original main calls other mehtods from their seperate scripts

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from pubsub import pub
import Tkinter as Tk
import tkMessageBox
from PIL import Image, ImageTk
import pyautogui
import time
import threading
import sys
import os

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
import click_callback as callback

#Find the screen width & set the approprite size for the feed
screenwidth, screenheight = pyautogui.size()

cap = cv2.VideoCapture(0)

########################################################################
class StartScreen(object):
    
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        global vidWidth
        global vidHeight
        vidWidth = (screenwidth/4)
        print 'vidWidth'
        print vidWidth
        vidHeight = (screenheight/4)
        
        if (sys.platform == 'win32'):
            extraW = 4
        elif (sys.platform == 'darwin'):
            extraW = 82


        w = vidWidth + extraW
        h = vidHeight + 60
        x = (screenwidth / 2) - (w / 2)
        y = (screenheight / 2) - (h / 2)
        
        self.root = parent
        self.root.title("Eye Tracker")
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.focus_force()
        self.frame = Tk.Frame(parent, width = w, height = h)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(rowspan = 5, columnspan = 4)
        self.buttonFrame = Tk.Frame(parent, width = w)
        self.buttonFrame.grid(row = 5, rowspan = 1, columnspan =5, sticky = 'S')

        welcomeLabel = Tk.Label(self.frame, text = "Welcome!", width = 44)
        global videoStreamInit
        #Create label for video to go in
        videoStreamInit = Tk.Label(self.frame)
        global calibrateButton
        calibrateButton = Tk.Button(self.buttonFrame, text="Calibrate", command=self.calibrationButton)
        helpButton = Tk.Button(self.buttonFrame, text = "Help", command=self.helpButton)
        quitButton = Tk.Button(self.buttonFrame, text="Quit", command=self.quitScreen)

        welcomeLabel.grid(row = 0, columnspan =4)
        videoStreamInit.grid(row = 1)
        calibrateButton.grid(row = 1, column = 0)
        helpButton.grid(row = 1, column = 3)
        quitButton.grid(row = 1, column = 4)
        
        global calButton
        calButton = False
        
        self.showInit()
    #----------------------------------------------------------------------
    #Show frame
    def show_frameInit(self):
        #Read the input feed, flip it, resize it and show it in the corresponding label
        #Original, flipped feed
        if cap.isOpened():
            #print 'Start frame'
            ret, frame = cap.read()
            #print 'frame open'
            flipFrame = cv2.flip(frame, 1)
            #cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2GRAY)
            cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight))
            img1 = Image.fromarray(cv2image)
            imgtk1 = ImageTk.PhotoImage(image=img1)
            videoStreamInit.imgtk1 = imgtk1
            videoStreamInit.configure(image=imgtk1)
            
            #Call the threholding function
            threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
            
            #Call Edge Detection of binary frame
            cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
            #Implement functionality that was used in main to draw around the pupil and glint
            #print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
            #print successfullyDetected
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
                if(frameCopy != None):
                    frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                    frameC_resized = cv2.flip(frameC_resized, 1)
                    img1 = Image.fromarray(frameC_resized)
                    imgtk1 = ImageTk.PhotoImage(image=img1)
                    videoStreamInit.imgtk1 = imgtk1
                    videoStreamInit.configure(image=imgtk1)
        else:
            videoStreamInit.configure(text = "You have not plugged in the camera")
            global cap
            cap = cv2.VideoCapture(0)

        if (not calButton):
                videoStreamInit.after(5, self.show_frameInit)

    #Update the frame
    def showInit(self):
        self.root.update()
        self.root.deiconify()
        self.show_frameInit()
    
    #----------------------------------------------------------------------
    #When the calibrate button is pressed
    def calibrationButton(self):
#        cap = cv2.VideoCapture(1)
#        if cap.isOpened():
        global calButton
        calButton = True
        self.openCalFrame()
#        else:
#            tkMessageBox.showwarning("No Eyetracker", "The eyetracker is not connected, please connect it.")

    def openCalFrame(self):
        cv2.destroyAllWindows()
        self.hide()
        global iteration
        iteration = 0
        pub.sendMessage("userFrameClosed", arg1="data")
        subFrame = CalibrationFrame()

    def hide(self):
        self.root.withdraw()

    #---------------------------------------------------------------------
    #When the help button is pressed
    def helpButton(self):
        print 'help button pressed'
        if (sys.platform == 'win32'):
            os.system('start <myFile>')
        elif (sys.platform == 'darwin'):
            os.system('open DIS_P05.pdf')

    #---------------------------------------------------------------------
    #When the quit button is pressed
    def quitScreen(self):
        cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
        self.root.destroy()


########################################################################
#The frame shown to allow the user to calibrate the system
class CalibrationFrame(Tk.Toplevel):
    #----------------------------------------------------------------------
    #GUI setup
    def __init__(self):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(screenwidth, screenheight))
        
        #Set up global variables
        global tWidth
        global tHeight
        
        #tWidth is the width of the screen divided by 3, this will be used to
        #calculate the x coordinates of the ovals
        tWidth = screenwidth/3
        
        #tHeight is the height of the screen divide by 3, used to calculate the
        #y coorindates of the ovals
        tHeight = screenheight/3
        
        #Set the size of the circle the user will look at
        dotSize = 26
        
        #Calculate the x and y coordinates for each of the nine circles
        #There are three x points, with 1 being the left most x point, and
        #3 being the rightmost
        #These x points are the x coordinate for the top left corner of the circle
        x1 = (np.mean([0, tWidth]) - (dotSize/2))
        x2 = x1 + tWidth
        x3 = x2 + tWidth
        
        #y1 is the top most y coordinate, y3 is the bottom most y coordinate
        y1 = (np.mean([0,tHeight]) - (dotSize/2))
        y2 = y1 + tHeight
        y3 = y2 +tHeight
        
        #Set up a list to hold all of the ovals on the screen
        global ovalList
        ovalList = []
        
        #Add frames and a canvas to the GUI
        canvasFrame = Tk.Frame(self, width = screenwidth, height = (screenheight - 100))
        instructionFrame = Tk.Frame(self, width = screenwidth, height = 50)
        self.canvas = Tk.Canvas(canvasFrame, width = screenwidth, height = (screenheight - 100))
        
        #Add the ovals to the canvas, and add each oval to the list
        oval1 = self.canvas.create_oval(x1, y1, (x1 + dotSize), (y1 + dotSize), fill = "grey") #top left
        ovalList.append(oval1)
        oval2 = self.canvas.create_oval(x2, y1, (x2 + dotSize), (y1 + dotSize), fill = "gray") #top middle
        ovalList.append(oval2)
        oval3 = self.canvas.create_oval(x3, y1, (x3 + dotSize), (y1 + dotSize), fill = "gray") #top right
        ovalList.append(oval3)
        
        oval4 = self.canvas.create_oval(x1, y2, (x1 + dotSize), (y2 + dotSize), fill = "gray") #middle left
        ovalList.append(oval4)
        oval5 = self.canvas.create_oval(x2, y2, (x2 + dotSize), (y2 + dotSize), fill = "gray") #middle middle
        ovalList.append(oval5)
        oval6 = self.canvas.create_oval(x3, y2, (x3 + dotSize), (y2 + dotSize), fill = "gray") #middle right
        ovalList.append(oval6)
        
        oval7 = self.canvas.create_oval(x1, y3, (x1 + dotSize), (y3 + dotSize), fill = "gray") #bottom left
        ovalList.append(oval7)
        oval8 = self.canvas.create_oval(x2, y3, (x2 + dotSize), (y3 + dotSize), fill = "gray") #bottom middle
        ovalList.append(oval8)
        oval9 = self.canvas.create_oval(x3, y3, (x3 + dotSize), (y3 + dotSize), fill = "gray") #botton right
        ovalList.append(oval9)
        
        #Set up all the global variables needed for calibration
        screenLocX1 = tWidth/2
        screenLocX2 = screenLocX1 + tWidth
        screenLocX3 = screenLocX2 + tWidth
        
        screenLocY1 = tHeight/2
        screenLocY2 = screenLocY1 + tHeight
        screenLocY3 = screenLocY2 + tHeight
        
        global screenCoordinatesX
        global screenCoordinatesY
        screenCoordinatesX = [screenLocX1, screenLocX2, screenLocX3,
                              screenLocX1, screenLocX2, screenLocX3,
                              screenLocX1, screenLocX2, screenLocX3]
                              
        screenCoordinatesY = [screenLocY1, screenLocY1, screenLocY1,
                              screenLocY2, screenLocY2, screenLocY2,
                              screenLocY3, screenLocY3, screenLocY3]
                              
        global pupilX
        global pupilY
        global glintX
        global glintY
        pupilX = []
        pupilY = []
        glintX = []
        glintY = []
      
        global iteration
        iteration = 0

        # create the button
        calibrateButton = Tk.Button(instructionFrame, text="Start Calibration", command=self.ovalChange)
        checkFeedButton = Tk.Button(instructionFrame, text = "Check Feed", command=self.checkFeedFrame)
        exitButton = Tk.Button(instructionFrame, text="Quit", command=self.checkQuitCal)
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        self.toplevel = None
        
        calibrateButton.grid(column = 0)
        checkFeedButton.grid(column = 1, row = 0)
        exitButton.grid(column = 2, row = 0)
        
        pub.subscribe(self.listener, "userFrameClosed")

        global quitButtonClick
        quitButtonClick = False
#
#    def globalVariables(self):
#            
#        print 'globals set'
    #--------------------------------------------------------------------
    #When the calibration button is pressed
    #Used to show which circle to look at, by displaying the circle in red
    def ovalChange(self):
        global iteration
        global quitButtonClick
        print "clicked start calibration %d" % iteration
        if (not quitButtonClick):
            # if iteration > 0:
                # prevOval = ovalList[iteration - 1]
                # self.canvas.itemconfigure(prevOval, fill="black")
            # if iteration < (len(ovalList)):
                # currentOval = ovalList[iteration]
                # self.canvas.itemconfigure(currentOval, fill="red")
            # self.canvas.update()
            # time.sleep(3)
            
            if iteration < (len(ovalList)):
                #Call Edge Detection of binary frame
				
                if iteration > 0:
                    prevOval = ovalList[iteration - 1]
                    self.canvas.itemconfigure(prevOval, fill="black")
				
                currentOval = ovalList[iteration]
                self.canvas.itemconfigure(currentOval, fill="red")
                self.canvas.update()
				
                count = 0
                while(count < 20):
                    count+=1
                    ret, frame = cap.read()
				
                gazeCount = 0
				
                curPupilX = []
                curPupilY = []
                curGlintX = []
                curGlintY = []
#                while (gazeCount < 3):
#                    countGap = 0
#                    while(countGap < 5):
#                        countGap+=1
#                        ret, frame = cap.read()
#                    ret, frame = cap.read()
#                    threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
#                    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
#                    calIteration = 0
#                    while not successfullyDetected:
#                        ret, frame = cap.read()
#                        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
#                        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
#                        calIteration += 1
#                        if calIteration > 100:
#                            self.canvas.itemconfigure(currentOval, fill="orange")
#                            self.canvas.update()
#                            threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
#                            cv2.imshow('feed',threshPupil)
#                    if successfullyDetected:
#						cv2.imwrite('pic{:>05}{}.png'.format(iteration, gazeCount), frame)
#						print ("saved image %d " % iteration)
#						calIteration = 0
#						curPupilX.append(cpX)
#						curPupilY.append(cpY)
#						curGlintX.append(ccX)
#						curGlintY.append(ccY)
#						# self.canvas.itemconfigure(currentOval, fill="green")
#						# self.canvas.update()
#					
#                    gazeCount += 1
#				
#                countPupilX = 0
#                for e in curPupilX:
#					countPupilX += e
#                avgPupilX = countPupilX/len(curPupilX)
#					
#                countPupilY = 0
#                for e in curPupilY:
#				    countPupilY += e
#                avgPupilY = countPupilY/len(curPupilY)
#				
#                countGlintX = 0
#                for e in curGlintX:
#					countGlintX += e
#                avgGlintX = countGlintX/len(curGlintX)
#					
#                countGlintY = 0
#                for e in curGlintY:
#					countGlintY += e
#                avgGlintY = countGlintY/len(curGlintY)
#				
#                pupilX.append(avgPupilX)
#                pupilY.append(avgPupilY)
#                glintX.append(avgGlintX)
#                glintY.append(avgGlintY)
#				
                iteration += 1
				
                if iteration == (len(ovalList)):
#                    global aOriginal
#                    global bOriginal
#                    aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY,screenCoordinatesX, screenCoordinatesY)
                    self.canvas.itemconfigure(currentOval, fill="black")
                    iteration += 1
                    self.openUserFrame()
                else:
                	self.ovalChange()
					#print 'pupilX current'
					#print pupilX
        
            # if iteration  < (len(ovalList)):
                

            # if iteration == (len(ovalList)):
                # global aOriginal
                # global bOriginal
                # aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY, screenCoordinatesX, screenCoordinatesY)
                # print 'iteration == lenOval'
                # iteration += 1
   # self.openUserFrame()
   
   #---------------------------------------------------------------------
    #Open the check feed frame
    def checkFeedFrame(self):
        if self.toplevel is None:
            self.toplevel = Tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW', self.removewindow)
            global vidWidth
            global vidHeight
            vidWidth = (screenwidth/4)
            vidHeight = (screenheight/4)
            
            #Set up how big the gui window should be, and where it should be positioned on screen
            #Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
            w = vidWidth + 4
            h = vidHeight + 4
            x = screenwidth - (w + 10)
            y = screenheight - (h + 60)
            
            #Set up the GUI
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))
            self.toplevel.title("Eye Tracking")
            #self.bind("<FocusOut>", self.hide)
            #self.bind("<Button-1>", self.hide)
            
            global videoStream1
            #Create label for video to go in
            videoStream1 = Tk.Label(self.toplevel)
            videoStream1.grid(row = 0, column = 0)
        
            self.show_frame()
        
        else:
            self.toplevel.lift()
#        print 'open check feed'
#        #self.hide()
#        subFrame = CheckFeedFrame()

#    #Hide the calibration frame
#    def hide(self):
#        self.withdraw()
    def removewindow(self):
        self.toplevel.destroy()
        self.toplevel = None

    #Show frame
    def show_frame(self):
        #Read the input feed, flip it, resize it and show it in the corresponding label
        #Original, flipped feed
        #print 'user frame'
        ret, frame = cap.read()
        flipFrame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2GRAY)
        cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight));
        img1 = Image.fromarray(cv2image)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        videoStream1.imgtk1 = imgtk1
        videoStream1.configure(image=imgtk1)
        
        #Call the threholding function
        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
        
        #Call Edge Detection of binary frame
        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
        #Implement functionality that was used in main to draw around the pupil and glint
        #print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
        #print successfullyDetected
        if cpX is None or cpY is None or ccX is None or ccY is None:
            print('pupil or corneal not detected, skipping...')
        #x = 1
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
            #----------------------------------------------------
            #Code that will hopefully show the detected pupil, if uncommented
            if(frameCopy != None):
                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                frameC_resized = cv2.flip(frameC_resized, 1)
                img1 = Image.fromarray(frameC_resized)
                imgtk1 = ImageTk.PhotoImage(image=img1)
                videoStream1.imgtk1 = imgtk1
                videoStream1.configure(image=imgtk1)


        videoStream1.after(5, self.show_frame)

    #---------------------------------------------------------------------
    #Open the user frame
    def openUserFrame(self):
        print 'open user frame'
        self.hide()
        subFrame = UserFrame()
    
    #Hide the calibration frame
    def hide(self):
        self.withdraw()
        if self.toplevel is not None:
            self.toplevel.withdraw()
    #----------------------------------------------------------------------
    #Called when exit is pressed
    def checkQuitCal(self):
        if (tkMessageBox.askokcancel("Quit", "Are you sure you want to quit?")):
            self.quitCal()

    def quitCal(self):
        global quitButtonClick
        quitButtonClick = True
        cap.release()
        cv2.destroyAllWindows()
        self.quit()
        self.destroy()

    #----------------------------------------------------------------------
    #When the user frame is closed, show the calibration screen
    def listener(self, arg1, arg2=None):
        print'Show calScreen'
        self.showCal()
    
    #Update the frame
    def showCal(self):
        self.update()
        self.deiconify()

########################################################################
#The frame shown when the user is interacting wiht the computer
class UserFrame(Tk.Toplevel):
    
    #----------------------------------------------------------------------
    #GUI setup
    def __init__(self):
        global vidWidth
        global vidHeight
        vidWidth = (screenwidth/4)
        vidHeight = (screenheight/4)

        #GUI setup
        Tk.Toplevel.__init__(self)
        
       #Calibration values
        # pupilX = [275, 264, 244, 280, 261, 239, 277, 259, 240]
        # pupilY = [178, 178, 178, 183, 183, 182, 188, 188, 190]
        # glintX = [278, 273, 264, 281, 272, 262, 279, 270, 259]
        # glintY = [190, 188, 190, 191, 189, 190, 190, 191, 192]
        # calibrationX = [213, 639, 1065, 213, 639, 1065, 213, 639, 1065]
        # calibrationY = [133, 133, 133, 399, 399, 399, 665, 665, 665]

        # global aOriginal
        # global bOriginal
        # aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY, calibrationX, calibrationY)
        
        #Set up how big the gui window should be, and where it should be positioned on screen
        #Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
        w = vidWidth + 4
        h = vidHeight + 56
        x = screenwidth - (w + 10)
        y = screenheight - (h + 60)
        
        #Set up the GUI
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("Eye Tracking")
        self.bind('<Escape>', self.checkQuitUser)
        self.protocol('WM_DELETE_WINDOW', self.checkQuitUser)
        
        #Create button frame
        buttonFrame = Tk.Frame(self)
        
        global videoStream1
        #Create label for video to go in
        videoStream1 = Tk.Label(self)
        
        global infoLabel
        infoLabel = Tk.Label(self)
        
        global moveCount
        moveCount = 0
        
        #Create buttons
        recalibrateButton = Tk.Button(buttonFrame, text = "Calibrate", command = self.recalibrate)
        quitButton = Tk.Button(buttonFrame, text = "Quit", command = self.checkQuitUser)
        
        #Put all of the elements into the GUI
        buttonFrame.grid(row = 2, column = 0, sticky = 'N')
        
        infoLabel.grid(row = 1, column = 0)
        videoStream1.grid(row = 0, column = 0)
        recalibrateButton.grid(row = 0, column = 0)
        quitButton.grid(row = 0, column = 1)
        
        self.show()
    
    #Show frame
    def show_frame(self):
        #Read the input feed, flip it, resize it and show it in the corresponding label
        #Original, flipped feed
        #print 'user frame'
        ret, frame = cap.read()
        flipFrame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2GRAY)
        cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight));
        img1 = Image.fromarray(cv2image)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        videoStream1.imgtk1 = imgtk1
        videoStream1.configure(image=imgtk1)
        
        #Call the threholding function
        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
        
        #Call Edge Detection of binary frame
        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
        #Implement functionality that was used in main to draw around the pupil and glint
        #print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
        #print successfullyDetected
        if cpX is None or cpY is None or ccX is None or ccY is None:
            print('pupil or corneal not detected, skipping...')
			#x = 1
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
            #----------------------------------------------------
            #Code that will hopefully show the detected pupil, if uncommented
            if(frameCopy != None):
                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                frameC_resized = cv2.flip(frameC_resized, 1)
                img1 = Image.fromarray(frameC_resized)
                imgtk1 = ImageTk.PhotoImage(image=img1)
                videoStream1.imgtk1 = imgtk1
                videoStream1.configure(image=imgtk1)
            
            global moveCount; global gazeXPrev; global gazeYPrev
			
            if 'aOriginal' in globals() and 'bOriginal' in globals():
                #print moveCount
                if (moveCount == 1):
					# Centre points of glint and pupil pass to vector
					gazeX, gazeY = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
					ATE.move_mouse(gazeX, gazeY)
					moveCount = 0
					
                else:
					moveCount += 1
					
                infoLabel.configure(text = "Now tracking your eye!")
            else:
                infoLabel.configure(text = "You have not calibrated yet, please do so")

        videoStream1.after(5, self.show_frame)

    #----------------------------------------------------------------------
    #Called when quit is pressed
    def checkQuitUser(self):
        if (tkMessageBox.askokcancel("Quit", "Are you sure you want to quit?")):
            self.quitUser()
    
    def quitUser(self):
        cap.release()
        cv2.destroyAllWindows()
        self.quit()
        self.destroy()
        
    #----------------------------------------------------------------------
    #Called when re-calibrate button is pressed
    #Send a message to pub to start the calibration again
    def recalibrate(self):
        cv2.destroyAllWindows()
        self.destroy()
        global iteration
        iteration = 0
        pub.sendMessage("userFrameClosed", arg1="data")

    #Update the frame
    def show(self):
        self.update()
        self.deiconify()
        self.show_frame()

########################################################################
##The frame shown to the user during calibration
#class CheckFeedFrame(Tk.Toplevel):
#    #----------------------------------------------------------------------
#    #GUI setup
#    def __init__(self):
#        global vidWidth
#        global vidHeight
#        vidWidth = (screenwidth/4)
#        vidHeight = (screenheight/4)
##        print 'win info'
##        print self.winfo_exists()
#
##        if 'normal' == self.state():
##            print 'running'
##        else
##            print 'not running'
#
#        if self.toplevel is None:
#            self.openWindow()
#
#    def openWindow(self):
#        #GUI setup
#        Tk.Toplevel.__init__(self)
#        
#        #Set up how big the gui window should be, and where it should be positioned on screen
#        #Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
#        w = vidWidth + 4
#        h = vidHeight + 4
#        x = screenwidth - (w + 10)
#        y = screenheight - (h + 60)
#        
#        #Set up the GUI
#        self.focus_set()
#        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
#        self.title("Eye Tracking")
#        self.bind("<FocusOut>", self.hide)
##self.bind("<Button-1>", self.hide)
#
#        global videoStream1
#        #Create label for video to go in
#        videoStream1 = Tk.Label(self)
#        videoStream1.grid(row = 0, column = 0)
#        
#        self.show()
#    
#    def hide(self, event):
##    #Hide the calibration frame
##    def hide(self):
#        self.destroy()
#
#    #Show frame
#    def show_frame(self):
#        #Read the input feed, flip it, resize it and show it in the corresponding label
#        #Original, flipped feed
#        #print 'user frame'
#        ret, frame = cap.read()
#        flipFrame = cv2.flip(frame, 1)
#        cv2image = cv2.cvtColor(flipFrame, cv2.COLOR_BGR2GRAY)
#        cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight));
#        img1 = Image.fromarray(cv2image)
#        imgtk1 = ImageTk.PhotoImage(image=img1)
#        videoStream1.imgtk1 = imgtk1
#        videoStream1.configure(image=imgtk1)
#        
#        #Call the threholding function
#        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
#        
#        #Call Edge Detection of binary frame
#        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
#        #Implement functionality that was used in main to draw around the pupil and glint
#        #print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
#        #print successfullyDetected
#        if cpX is None or cpY is None or ccX is None or ccY is None:
#            print('pupil or corneal not detected, skipping...')
#        #x = 1
#        else:
#            # Ellipse Fitting
#            frameCopy = frame.copy()
#            
#            #draw pupil centre
#            cv2.circle(frameCopy, (cpX,cpY),3,(0,255,0),-1)
#            
#            #draw pupil circumference
#            cv2.drawContours(frameCopy,cp,-1,(0,0,255),3)
#            
#            #draw corneal centre
#            cv2.circle(frameCopy, (ccX,ccY),3,(0,255,0),-1)
#            
#            #draw corneal circumference
#            cv2.drawContours(frameCopy,cc,-1,(0,0,255),3)
#            #----------------------------------------------------
#            #Code that will hopefully show the detected pupil, if uncommented
#            if(frameCopy != None):
#                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
#                frameC_resized = cv2.flip(frameC_resized, 1)
#                img1 = Image.fromarray(frameC_resized)
#                imgtk1 = ImageTk.PhotoImage(image=img1)
#                videoStream1.imgtk1 = imgtk1
#                videoStream1.configure(image=imgtk1)
#            
#                                            
#        videoStream1.after(5, self.show_frame)
#
#    #Update the frame
#    def show(self):
#        self.update()
#        self.deiconify()
#        self.show_frame()
#
########################################################################


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    app = StartScreen(root)
    root.mainloop()
    cap.release()