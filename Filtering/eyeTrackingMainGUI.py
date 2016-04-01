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
from PIL import Image, ImageTk
import pyautogui
import time
import threading

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

cap = cv2.VideoCapture(1)
capOpen = cap.isOpened()

########################################################################
class StartScreen(object):
    
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        w = 400
        h = 200
        x = (screenwidth / 2) - (w / 2)
        y = (screenheight / 2) - (h / 2)
        
        self.root = parent
        self.root.title("Welcome")
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.focus_force()
        self.frame = Tk.Frame(parent, width = w, height = h)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(rowspan = 5, columnspan = 4)
        self.buttonFrame = Tk.Frame(parent, width = w)
        self.buttonFrame.grid(row = 5, rowspan = 1, columnspan = 4, sticky = 'S')
        
#        global curState
#        if cap.isOpened():
#            curState = 'normal'
#        else:
#            curState = 'disabled'

        welcomeLabel = Tk.Label(self.frame, text = "Welcome!", width = 44)
        global calibrateButton
        calibrateButton = Tk.Button(self.buttonFrame, text="Calibrate", command=self.openCalFrame)
        quitButton = Tk.Button(self.buttonFrame, text="Quit", command=self.quitScreen)
        welcomeLabel.grid(row = 0, columnspan =4)
        
        calibrateButton.grid(row = 1, column = 2)
        quitButton.grid(row = 1, column = 3)

#        self.getCurState()

#    def getCurState(self):
#        global curState
#        thread = threading.Timer(5.0, self.getCurState).start()
#        cap = cv2.VideoCapture(1)
#        if cap.isOpened():
#            curState = 'normal'
#            thread.stop()
#        else:
#            curState = 'disabled'
#        print curState
#        calibrateButton.configure(state = curState)

    #----------------------------------------------------------------------
    #When the calibrate button is pressed
    def openCalFrame(self):
        self.hide()
        subFrame = CalibrationFrame()
    
    def hide(self):
        self.root.withdraw()
    
    #---------------------------------------------------------------------
    #When the quit button is pressed
    def quitScreen(self):
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
        userButton = Tk.Button(instructionFrame, text = "User Frame", command=self.openUserFrame)
        exitButton = Tk.Button(instructionFrame, text="Quit", command=self.quitCal)
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        
        calibrateButton.grid(column = 0)
        userButton.grid(column = 1, row = 0)
        exitButton.grid(column = 2, row = 0)
        
        pub.subscribe(self.listener, "userFrameClosed")
    
    
    def globalVariables(self):
            
        print 'globals set'
    #----------------------------------------------------------------------
    #Called when exit is pressed
    def quitCal(self):
        self.quit()
        self.destroy()
    
    #--------------------------------------------------------------------
    #When the calibration button is pressed
    #Used to show which circle to look at, by displaying the circle in red
    def ovalChange(self):
        global iteration
        print iteration
        if iteration > 0:
            prevOval = ovalList[iteration - 1]
            self.canvas.itemconfigure(prevOval, fill="black")
        if iteration < (len(ovalList)):
            currentOval = ovalList[iteration]
            self.canvas.itemconfigure(currentOval, fill="red")
        self.canvas.update()
        time.sleep(3)
        
        if iteration < (len(ovalList)):
            #Call Edge Detection of binary frame
            ret, frame = cap.read()
            threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
            cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
            calIteration = 0
            while not successfullyDetected:
                ret, frame = cap.read()
                threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
                cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
                calIteration += 1
                #print calIteration
                if calIteration > 100:
                    self.canvas.itemconfigure(currentOval, fill="orange")
                    self.canvas.update()
                    threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
                    cv2.imshow('feed',threshPupil)
            if successfullyDetected:
                cv2.imwrite('pic{:>05}.png'.format(iteration), frame)
                calIteration = 0
                pupilX.append(cpX)
                pupilY.append(cpY)
                glintX.append(ccX)
                glintY.append(ccY)
                #print 'pupilX current'
                #print pupilX
    
        if iteration  < (len(ovalList)):
            iteration += 1
            self.ovalChange()

        if iteration == (len(ovalList)):
            global aOriginal
            global bOriginal
            aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY, screenCoordinatesX, screenCoordinatesY)
            print 'iteration == lenOval'
            iteration += 1
            self.openUserFrame()
    
    #Open the user frame
    def openUserFrame(self):
        print 'open user frame'
        self.hide()
        subFrame = UserFrame()
    
    #Hide the calibration frame
    def hide(self):
        self.withdraw()
    
    #----------------------------------------------------------------------
    #When the user frame is closed, show the calibration screen
    def listener(self, arg1, arg2=None):
        print'Show calScreen'
        self.show()
    
    #Update the frame
    def show(self):
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

        print 'user frame opned'
        Tk.Toplevel.__init__(self)
        #Capture the feed coming from the camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, vidWidth)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vidHeight)

#        #Calibration values
#        pupilX = [275, 264, 244, 280, 261, 239, 277, 259, 240]
#        pupilY = [178, 178, 178, 183, 183, 182, 188, 188, 190]
#        glintX = [278, 273, 264, 281, 272, 262, 279, 270, 259]
#        glintY = [190, 188, 190, 191, 189, 190, 190, 191, 192]
#        calibrationX = [213, 639, 1065, 213, 639, 1065, 213, 639, 1065]
#        calibrationY = [133, 133, 133, 399, 399, 399, 665, 665, 665]
#
#        global aOriginal
#        global bOriginal
#        aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY, calibrationX, calibrationY)

        #Set up how big the gui window should be, and where it should be positioned on screen
        #Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
        w = vidWidth + 4
        h = vidHeight + 34
        x = screenwidth - (w + 10)
        y = screenheight - (h + 60)

        #Set up the GUI
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("Eye Tracking")
        self.bind('<Escape>', quit)

        #Create button frame
        buttonFrame = Tk.Frame(self)

        global videoStream1
        #Create label for video to go in
        videoStream1 = Tk.Label(self)

        #Create buttons
        recalibrateButton = Tk.Button(buttonFrame, text = "Recalibrate", command = self.recalibrate)
        quitButton = Tk.Button(buttonFrame, text = "Quit", command = self.quitCal)

        #Put all of the elements into the GUI
        buttonFrame.grid(row = 1, column = 0, sticky = 'N')

        videoStream1.grid(row = 0, column = 0)
        recalibrateButton.grid(row = 0, column = 0)
        quitButton.grid(row = 0, column = 1)
    
        self.show()

    #Show frame
    def show_frame(self):
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
            if(frameCopy != None):
                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                frameC_resized = cv2.flip(frameC_resized, 1)
                img1 = Image.fromarray(frameC_resized)
                imgtk1 = ImageTk.PhotoImage(image=img1)
                videoStream1.imgtk1 = imgtk1
                videoStream1.configure(image=imgtk1)

            # Centre points of glint and pupil pass to vector
            x, y = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
    
            # Coordinates on screen
            ATE.move_mouse(x,y)
    
        videoStream1.after(5, self.show_frame)

    #----------------------------------------------------------------------
    #Called when quit is pressed
    def quitCal(self):
        self.quit()
        self.destroy()
        
    #----------------------------------------------------------------------
    #Called when re-calibrate button is pressed
    #Send a message to pub to start the calibration again
    def recalibrate(self):
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


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    app = StartScreen(root)
    root.mainloop()
    cap.release()