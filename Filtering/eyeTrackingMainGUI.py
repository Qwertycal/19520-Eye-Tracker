#author: Rachel Hutchinson implements code written by Nadezhda Shivarova, Calum Whytock and David McNicol
#date created: 28th March
#description: shows the original feed, and has three buttons, one with the option to
#Calibrate the system, one to show a help file and the other with the option to quit
#This includes the code from the original main and calls other methods from their separate scripts

#Import necessary packages
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from pubsub import pub as Publisher
import Tkinter as Tk
import tkMessageBox
from PIL import Image, ImageTk
import pyautogui
import time
import threading
import sys
import os
import FileDialog

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

#Find the screen width & height
screenwidth, screenheight = pyautogui.size()

#Set the input capture port, depending on the system
if (sys.platform == 'win32'):
    capVal = 0
elif (sys.platform == 'darwin'):
    capVal = 1
cap = cv2.VideoCapture(capVal)

########################################################################
#The screen shown when the system is started
class StartScreen(object):
    
    #----------------------------------------------------------------------
    #GUI set up
    def __init__(self, parent):
        
        #Set the size of the video feed to be shown, relevant to the screen size
        global vidWidth
        global vidHeight
        vidWidth = (screenwidth/4)
        vidHeight = (screenheight/4)
        
        #Set up variables which specify the size and position of the user frame
        #w and h set width and height of frame
        #x and y set the position of the top corner of the frame
        w = vidWidth + 4
        h = vidHeight + 60
        x = (screenwidth / 2) - (w / 2)
        y = (screenheight / 2) - (h / 2)
        
        #Set up the GUI and add frames
        self.root = parent
        self.root.title("Eye Tracker")
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.focus_force()
        self.frame = Tk.Frame(parent, width = w, height = h)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(rowspan = 5, columnspan = 4)
        self.buttonFrame = Tk.Frame(parent, width = w)
        self.buttonFrame.grid(row = 5, rowspan = 1, columnspan =5, sticky = 'S')

        #Add a welcome lable
        welcomeLabel = Tk.Label(self.frame, text = "Welcome!", width = 44)
        global videoStreamInit
        #Create label for video to go in
        videoStreamInit = Tk.Label(self.frame)
        #Add buttons
        global calibrateButton
        calibrateButton = Tk.Button(self.buttonFrame, text="Calibrate", command=self.calibrationButton)
        helpButton = Tk.Button(self.buttonFrame, text = "Help", command=self.helpButton)
        quitButton = Tk.Button(self.buttonFrame, text="Quit", command=self.quitScreen)

        #Add all GUI elements to GUI
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
        if cap.isOpened():
            ret, frame = cap.read()
            flipFrame = cv2.flip(frame, 1)
            cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight))
            img1 = Image.fromarray(cv2image)
            imgtk1 = ImageTk.PhotoImage(image=img1)
            videoStreamInit.imgtk1 = imgtk1
            videoStreamInit.configure(image=imgtk1)
            
            #Call the threholding function
            threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
            
            #Call Edge Detection of binary frame
            cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
            #Draw around the pupil and glint, if they are detected
            print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
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
                
                #Code that will show the detected pupil, if it is detected
                if(frameCopy != None):
                    frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                    frameC_resized = cv2.flip(frameC_resized, 1)
                    img1 = Image.fromarray(frameC_resized)
                    imgtk1 = ImageTk.PhotoImage(image=img1)
                    videoStreamInit.imgtk1 = imgtk1
                    videoStreamInit.configure(image=imgtk1)
        else:
            #Alerts the suer if the camera is not plugged in, attempts to open camera feed
            videoStreamInit.configure(text = "You have not plugged in the camera")
            global cap
            cap = cv2.VideoCapture(capVal)

        #Continue showing feed until calibration button is pressed.
        if (not calButton):
                videoStreamInit.after(5, self.show_frameInit)

    #Update the frame
    def showInit(self):
        self.root.update()
        self.root.deiconify()
        self.show_frameInit()
    
    #----------------------------------------------------------------------
    #When the calibrate button is pressed
    #Check if the camera is connected, giva a warning if it is not
    def calibrationButton(self):
        if cap.isOpened():
            global calButton
            calButton = True
            self.openCalFrame()
        else:
            tkMessageBox.showwarning("No Eyetracker", "The eyetracker is not connected, please connect it.")

    #Destroys the start frame, sends message that calibration frame should be shown
    def openCalFrame(self):
        cv2.destroyAllWindows()
        self.hide()
        global iteration
        iteration = 0
        Publisher.sendMessage("userFrameClosed", arg1="data")
        subFrame = CalibrationFrame()

    def hide(self):
        self.root.withdraw()

    #---------------------------------------------------------------------
    #When the help button is pressed
    #Show the user guide, different method, depending on operating system
    def helpButton(self):
        print 'help button pressed'
        if (sys.platform == 'win32'):
            os.system('start UserGuide.pdf')
        elif (sys.platform == 'darwin'):
            os.system('open UserGuide.pdf')

    #---------------------------------------------------------------------
    #When the quit button is pressed
    #Destroy all windows and quit
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
        #Make the GUI fullscreen
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
        #Store the x and y coordniates of the centre point of the dots
        screenLocX1 = tWidth/2
        screenLocX2 = screenLocX1 + tWidth
        screenLocX3 = screenLocX2 + tWidth
        
        screenLocY1 = tHeight/2
        screenLocY2 = screenLocY1 + tHeight
        screenLocY3 = screenLocY2 + tHeight
        
        global screenCoordinatesX
        global screenCoordinatesY
        #Store the coordinates in order in a list
        screenCoordinatesX = [screenLocX1, screenLocX2, screenLocX3,
                              screenLocX1, screenLocX2, screenLocX3,
                              screenLocX1, screenLocX2, screenLocX3]
                              
        screenCoordinatesY = [screenLocY1, screenLocY1, screenLocY1,
                              screenLocY2, screenLocY2, screenLocY2,
                              screenLocY3, screenLocY3, screenLocY3]
        
        #Set up lists for the different coordinates required for the calibration equations
        global pupilX
        global pupilY
        global glintX
        global glintY
        pupilX = []
        pupilY = []
        glintX = []
        glintY = []
      
        #Set up a variable that keeps track of the iteration (determines which dot is lit up)
        global iteration
        iteration = 0

        #Create the buttons
        calibrateButton = Tk.Button(instructionFrame, text="Start Calibration", command=self.ovalChange)
        checkFeedButton = Tk.Button(instructionFrame, text = "Check Feed", command=self.checkFeedFrame)
        exitButton = Tk.Button(instructionFrame, text="Quit", command=self.checkQuitCal)
        
        #Put the widgets in the GUI
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        self.toplevel = None
        
        calibrateButton.grid(column = 0)
        checkFeedButton.grid(column = 1, row = 0)
        exitButton.grid(column = 2, row = 0)
        
        #Listen for when the start or user frame is closed
        Publisher.subscribe(self.listener, "userFrameClosed")
        
        #Keep track of if the quit button has been pressed
        global quitButtonClick
        quitButtonClick = False

    #--------------------------------------------------------------------
    #When the calibration button is pressed
    
    #Used to show which circle to look at, by displaying the circle in red
    def ovalChange(self):
        global iteration
        global quitButtonClick
        print "clicked start calibration %d" % iteration
        #As long as the quit button hasnt been pressed
        #Colour the previous dot black, if there is a previous dot
        #Colour the current dot red
        if (not quitButtonClick):
            if iteration > 0:
                prevOval = ovalList[iteration - 1]
                self.canvas.itemconfigure(prevOval, fill="black")
            if iteration < (len(ovalList)):
                currentOval = ovalList[iteration]
                self.canvas.itemconfigure(currentOval, fill="red")
            self.canvas.update()
            time.sleep(3)
            
            if iteration < (len(ovalList)):
                if iteration > 0:
                    prevOval = ovalList[iteration - 1]
                    self.canvas.itemconfigure(prevOval, fill="black")
                
                currentOval = ovalList[iteration]
                self.canvas.itemconfigure(currentOval, fill="red")
                self.canvas.update()
                
                #Cause a delay between dots, so the user has time to move gaze
                count = 0
                while(count < 12):
                    count+=1
                    ret, frame = cap.read()
                
                gazeCount = 0
                
                curPupilX = []
                curPupilY = []
                curGlintX = []
                curGlintY = []
                #Collect 3 sets of gaze points for each dot
                while (gazeCount < 3):
                    countGap = 0
                    #Cause delay between collection of data sets
                    while(countGap < 4):
                        countGap+=1
                        ret, frame = cap.read()
                    #Read frame, threshold, edge detect
                    ret, frame = cap.read()
                    threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
                    cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
                    calIteration = 0
                    #If edges have not been detected, try again
                    #If edges are not detected for a prolonged perios, turn calibration dot orange
                    #and show the camera feed
                    while not successfullyDetected:
                        ret, frame = cap.read()
                        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
                        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
                        calIteration += 1
                        if calIteration > 100:
                            self.canvas.itemconfigure(currentOval, fill="orange")
                            self.canvas.update()
                            threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
                            self.checkFeedFrame()
                    
                    #If the edges have been successfully detected, store the pupil and glint data
                    if successfullyDetected:
                        self.removewindow()
                        cv2.imwrite('pic{:>05}{}.png'.format(iteration, gazeCount), frame)
                        print ("saved image %d " % iteration)
                        calIteration = 0
                        curPupilX.append(cpX)
                        curPupilY.append(cpY)
                        curGlintX.append(ccX)
                        curGlintY.append(ccY)
                        # self.canvas.itemconfigure(currentOval, fill="green")
                        # self.canvas.update()
                    
                    gazeCount += 1
                
                #Once there are three sets of gaze data for each dot
                #find the average values of each bit of data and store the average
                #in the corresponding list
                countPupilX = 0
                for e in curPupilX:
                    countPupilX += e
                avgPupilX = countPupilX/len(curPupilX)
                    
                countPupilY = 0
                for e in curPupilY:
                    countPupilY += e
                avgPupilY = countPupilY/len(curPupilY)
                
                countGlintX = 0
                for e in curGlintX:
                    countGlintX += e
                avgGlintX = countGlintX/len(curGlintX)
                    
                countGlintY = 0
                for e in curGlintY:
                    countGlintY += e
                avgGlintY = countGlintY/len(curGlintY)
                
                pupilX.append(avgPupilX)
                pupilY.append(avgPupilY)
                glintX.append(avgGlintX)
                glintY.append(avgGlintY)
                
                iteration += 1
                
                #If all the dots have been visited pass the data collected to the
                #calibraiton equations and open the user frame
                if iteration == (len(ovalList)):
                    global aOriginal
                    global bOriginal
                    aOriginal, bOriginal =  GCU.calibration(pupilX, pupilY, glintX, glintY,screenCoordinatesX, screenCoordinatesY)
                    self.canvas.itemconfigure(currentOval, fill="black")
                    iteration += 1
                    self.openUserFrame()
                else:
                    self.ovalChange()
   
   #---------------------------------------------------------------------
    #Open the check feed frame
    def checkFeedFrame(self):
        #If the check feed frame doesn't exisit create one
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
            
            global videoStream1
            #Create label for video to go in
            videoStream1 = Tk.Label(self.toplevel)
            videoStream1.grid(row = 0, column = 0)
        
            #Show the video stream
            self.show_frame()
        
        #If the frame already exists show it
        else:
            print 'lift'
            self.toplevel.focus_force()
            self.toplevel.lift()
    
    #Called when the pupil is detected for the calibraiton dot
    #Destryos the window if it exists
    def removewindow(self):
        try:
            self.toplevel.destroy()
            self.toplevel = None
        except:
            print'No toplevel'

    def show_frame(self):
        #Read the input feed, flip it, resize it and show it in the corresponding label
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
        #Draw around the pupil and glint
        print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
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
            #Show the detected pupil
            if(frameCopy != None):
                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                frameC_resized = cv2.flip(frameC_resized, 1)
                img1 = Image.fromarray(frameC_resized)
                imgtk1 = ImageTk.PhotoImage(image=img1)
                videoStream1.imgtk1 = imgtk1
                videoStream1.configure(image=imgtk1)

        videoStream1.after(5, self.show_frame)

    #---------------------------------------------------------------------
    #Once calibraiton has finished
    #Open the user frame
    def openUserFrame(self):
        print 'open user frame'
        self.hide()
        subFrame = UserFrame()
    
    #Hide the calibration frame
    def hide(self):
        self.withdraw()
        if self.toplevel is not None:
            print 'toplevel destroy'
            self.toplevel.destroy()

    #----------------------------------------------------------------------
    #Called when exit is pressed
    #Check the user wants to quit
    def checkQuitCal(self):
        if (tkMessageBox.askokcancel("Quit", "Are you sure you want to quit?")):
            self.quitCal()
    #Set the quitButtonClick to true, to stop the calibraiotn process
    #Destroy all windows and quit
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
#The frame shown when the user is interacting with the computer
class UserFrame(Tk.Toplevel):
    #GUI setup
    def __init__(self):
        global vidWidth
        global vidHeight
        vidWidth = (screenwidth/4)
        vidHeight = (screenheight/4)

        #GUI setup
        Tk.Toplevel.__init__(self)
 
        #Set up how big the gui window should be, and where it should be positioned on screen
        #Set to be slightly bigger than the video feed, and be positioned in the bottom right of the screen
        w = vidWidth + 4
        h = vidHeight + 56
        #Set the height, depending on the OS
        if (sys.platform == 'win32'):
            y = screenheight - (h + 70)
        elif (sys.platform == 'darwin'):
            y = screenheight - (h + 60)
        x = screenwidth - (w + 10)
        
        #Set the mouseToggle
        global mouseToggle 
        mouseToggle = True
        
        #Set up the GUI
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("Eye Tracking")
        self.bind('<Escape>', self.checkEscapeQuitUser)
        self.bind('m', self.mouseControlToggle)
        self.protocol('WM_DELETE_WINDOW', self.checkQuitUser)
        
        #Create button frame
        buttonFrame = Tk.Frame(self)
        
        #Create label for video to go in
        global videoStream1
        videoStream1 = Tk.Label(self)
        
        global infoLabel
        infoLabel = Tk.Label(self)
        
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
    
    #----------------------------------------------------------------------
    #Show frame
    def show_frame(self):
        #Read the input feed, flip it, resize it and show it in the corresponding label
        ret, frame = cap.read()
        flipFrame = cv2.flip(frame, 1)
        cv2image = cv2.resize(flipFrame, (vidWidth, vidHeight));
        img1 = Image.fromarray(cv2image)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        videoStream1.imgtk1 = imgtk1
        videoStream1.configure(image=imgtk1)
        
        #Call the threholding function
        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
        
        #Call Edge Detection of binary frame
        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
        #Draw around the pupil and glint
        print('cpX: ', cpX, ' cpY: ', cpY, ' ccX: ', ccX, ' ccY: ', ccY)
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
           
            #Show detected pupil
            if(frameCopy != None):
                frameC_resized = cv2.resize(frameCopy, (vidWidth, vidHeight), interpolation = cv2.INTER_AREA)
                frameC_resized = cv2.flip(frameC_resized, 1)
                img1 = Image.fromarray(frameC_resized)
                imgtk1 = ImageTk.PhotoImage(image=img1)
                videoStream1.imgtk1 = imgtk1
                videoStream1.configure(image=imgtk1)
            
            #If mouseToggle is true implement the cursor control code
            #Allows user to interact with computer wiht their eyes
            if mouseToggle:
                if 'aOriginal' in globals() and 'bOriginal' in globals():
                    # Centre points of glint and pupil pass to vector
                    gazeX, gazeY = GGP.getGazePoint(aOriginal, bOriginal, cpX, cpY, ccX, ccY)
                    ATE.move_mouse(gazeX, gazeY)
                    infoLabel.configure(text = "Now tracking your eye!")
                else:
                    infoLabel.configure(text = "You have not calibrated yet, please do so")

        videoStream1.after(5, self.show_frame)
    
    #----------------------------------------------------------------------
    #Toggle cursor control
    #If mouseToggle is true, cursor is controlled through eye tracker
    #If mouseToggle is false, cursor is controlled wiht mouse
    def mouseControlToggle(self, event):
        global mouseToggle
        print 'm pressed'
        if mouseToggle:
            mouseToggle = False
            print 'MCT false'
        else:
            mouseToggle = True
            print 'MCT true'
    #----------------------------------------------------------------------
    #Called when quit or 'Esc' is pressed
    #Check the user wants to quit
    def checkQuitUser(self):
        if (tkMessageBox.askokcancel("Quit", "Are you sure you want to quit?")):
            self.quitUser()
    def checkEscapeQuitUser(self, Event):
        if (tkMessageBox.askokcancel("Quit", "Are you sure you want to quit?")):
            self.quitUser()
    #Destroy all windows and quit
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
        Publisher.sendMessage("userFrameClosed", arg1="data")

    #----------------------------------------------------------------------
    #Update the frame
    def show(self):
        self.update()
        self.deiconify()
        self.show_frame()

########################################################################
if __name__ == "__main__":
    root = Tk.Tk()
    app = StartScreen(root)
    root.mainloop()
    cap.release()