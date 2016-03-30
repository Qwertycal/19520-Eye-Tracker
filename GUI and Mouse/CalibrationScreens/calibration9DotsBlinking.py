#author: Rachel Hutchinson
#date created: 25th March
#description: this holds the calibration scrren, when you press the start calibration button
#each of the 9 calibration dos will light up in turn, this will call the image thresholding
#and edge detection mehtods
from Tkinter import *
import cv2
import pyautogui
import numpy
import time

class MyApp(Tk):
    #Set up GUI
    def __init__(self):
        Tk.__init__(self)
        #Make GUI full screen
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        
        #Find size of screen
        width, height = pyautogui.size() #get the width and height of the screen
        print(width)
        print(height)
        
        #Set up global variables
        global qWidth
        global tHeight
        
        #qWidth is the width of the screen divided by 3, this will be used to
        #calculate the x coordinates of the ovals
        qWidth = width/3
        
        #tHeight is the height of the screen divide by 3, used to calculate the
        #y coorindates of the ovals
        tHeight = height/3
        
        #Set the size of the circle the user will look at
        dotSize = 26
        
        #Calculate the x and y coordinates for each of the nine circles
        #There are three x points, with 1 being the left most x point, and
        #3 being the rightmost
        #These x points are the x coordinate for the top left corner of the circle
        x1 = (numpy.mean([0, qWidth]) - (dotSize/2))
        x2 = x1 + qWidth
        x3 = x2 + qWidth
        
        #y1 is the top most y coordinate, y3 is the bottom most y coordinate
        y1 = (numpy.mean([0,tHeight]) - (dotSize/2))
        y2 = y1 + tHeight
        y3 = y2 +tHeight
        
        #Set up a list to hold all of the ovals on the screen
        global ovalList
        ovalList = []
        
        #Add frames and a canvas to the GUI
        canvasFrame = Frame(self, width = width, height = (height - 100))
        instructionFrame = Frame(self, width = width, height = 50)
        self.canvas = Canvas(canvasFrame, width = width, height = (height - 100))
        
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
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        
        #Set up the buttons and the actions linked to them
        i = 0
        calibrateButton = Button(instructionFrame, text="Start Calibration", command=self.ovalChanger)
        exitButton = Button(instructionFrame, text="Exit", command=self.quitCal)
        calibrateButton.grid(column = 0)
        exitButton.grid(column = 1, row = 0)
    
    #Called when exit is pressed
    def quitCal(self):
        self.destroy()
    
    #Called when the calibrate button is pressed, simply used to call another funtion
    def ovalChanger(self):
        self.ovalChange(0)
    
    #Used to show which circle to look at, by displaying the circle in red
    def ovalChange(self, i):
        if i > 0:
            prevOval = ovalList[i - 1]
            self.canvas.itemconfigure(prevOval, fill="black")
        if i < (len(ovalList)):
            currentOval = ovalList[i]
            self.canvas.itemconfigure(currentOval, fill="red")
        self.canvas.update()
        time.sleep(5)
        
        #Call Edge Detection of binary frame
        ret, frame = cap.read()
        threshPupil, threshGlint = imgThreshold.imgThreshold(frame)
        cpX,cpY,cp,ccX,ccY,cc,successfullyDetected = edgeDet.edgeDetectionAlgorithm(threshPupil,threshGlint)
        cv2.imwrite('pic{:>05}.png'.format(i), frame)
        
        if i  < (len(ovalList)):
            j = i + 1
            self.ovalChange(j)

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    root = MyApp()
    root.mainloop()