from Tkinter import *
import cv2
import pyautogui
import numpy
import time

class MyApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        
        width, height = pyautogui.size() #get the width and height of the screen
        print(width)
        print(height)
        
        global qWidth
        global tHeight
        qWidth = width/3
        tHeight = height/3
        
        dotSize = 26
        x1 = (numpy.mean([0, qWidth]) - (dotSize/2))
        y1 = (numpy.mean([0,tHeight]) - (dotSize/2))
        x2 = x1 + qWidth
        x3 = x2 + qWidth
        
        y2 = y1 + tHeight
        y3 = y2 +tHeight
        
        global ovalList
        ovalList = []
        
        canvasFrame = Frame(self, bg = "red", width = width, height = (height - 100))
        instructionFrame = Frame(self, width = width, height = 50)
        self.canvas = Canvas(canvasFrame, width = width, height = (height - 100))
        
        self.oval1 = self.canvas.create_oval(x1, y1, (x1 + dotSize), (y1 + dotSize), fill = "grey") #top left
        ovalList.append(self.oval1)
        self.oval2 = self.canvas.create_oval(x2, y1, (x2 + dotSize), (y1 + dotSize), fill = "gray") #top middle
        ovalList.append(self.oval2)
        self.oval3 = self.canvas.create_oval(x3, y1, (x3 + dotSize), (y1 + dotSize), fill = "gray") #top right
        ovalList.append(self.oval3)
        
        self.oval4 = self.canvas.create_oval(x1, y2, (x1 + dotSize), (y2 + dotSize), fill = "gray") #middle left
        ovalList.append(self.oval4)
        self.oval5 = self.canvas.create_oval(x2, y2, (x2 + dotSize), (y2 + dotSize), fill = "gray") #middle second left
        ovalList.append(self.oval5)
        self.oval6 = self.canvas.create_oval(x3, y2, (x3 + dotSize), (y2 + dotSize), fill = "gray") #middle third left
        ovalList.append(self.oval6)
        
        self.oval7 = self.canvas.create_oval(x1, y3, (x1 + dotSize), (y3 + dotSize), fill = "gray") #bottom left
        ovalList.append(self.oval7)
        self.oval8 = self.canvas.create_oval(x2, y3, (x2 + dotSize), (y3 + dotSize), fill = "gray") #bottom middle
        ovalList.append(self.oval8)
        self.oval9 = self.canvas.create_oval(x3, y3, (x3 + dotSize), (y3 + dotSize), fill = "gray") #botton right
        ovalList.append(self.oval9)
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        
        i = 0
        self.start_button = Button(instructionFrame, text="Start Calibration", command=self.ovalChanger)
        self.stop_button = Button(instructionFrame, text="Exit", command=self.stop_blinking)
        self.start_button.grid(column = 0)
        self.stop_button.grid(column = 1, row = 0)
    
    #global calCircle
    #calCircle = 1
    
    def ovalChanger(self):
        self.ovalChange(0)
    
    def ovalChange(self, i):
        print ('Oval Change')
        print i
        if i > 0:
            self.prevOval = ovalList[i - 1]
            self.canvas.itemconfigure(self.prevOval, fill="black")
        if i < (len(ovalList)):
            self.currentOval = ovalList[i]
            self.canvas.itemconfigure(self.currentOval, fill="red")
        self.canvas.update()
        time.sleep(5)
        if i  < (len(ovalList)):
            j = i + 1
            self.ovalChange(j)

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    root = MyApp()
    root.mainloop()