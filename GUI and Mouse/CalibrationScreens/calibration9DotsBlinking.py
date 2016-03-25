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
        global q3Width
        qWidth = width/3
        tHeight = height/3
        
        dotSize = 26
        x1 = (numpy.mean([0, qWidth]) - (dotSize/2))
        y1 = (numpy.mean([0,tHeight]) - (dotSize/2))
        x2 = x1 + qWidth
        x3 = x2 + qWidth
        
        y2 = y1 + tHeight
        y3 = y2 +tHeight
        
        canvasFrame = Frame(self, bg = "red", width = width, height = (height - 100))
        instructionFrame = Frame(self, width = width, height = 50)
        self.canvas = Canvas(canvasFrame, width = width, height = (height - 100))
        
        self.oval1 = self.canvas.create_oval(x1, y1, (x1 + dotSize), (y1 + dotSize), outline = "grey", fill = "grey") #top left
        self.oval2 = self.canvas.create_oval(x2, y1, (x2 + dotSize), (y1 + dotSize), outline = "gray", fill = "gray") #top middle
        self.oval3 = self.canvas.create_oval(x3, y1, (x3 + dotSize), (y1 + dotSize), outline = "gray", fill = "gray") #top right
    
        self.oval4 = self.canvas.create_oval(x1, y2, (x1 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle left
        self.oval5 = self.canvas.create_oval(x2, y2, (x2 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle second left
        self.oval6 = self.canvas.create_oval(x3, y2, (x3 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle third left
        
        self.oval7 = self.canvas.create_oval(x1, y3, (x1 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #bottom left
        self.oval8 = self.canvas.create_oval(x2, y3, (x2 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #bottom middle
        self.oval9 = self.canvas.create_oval(x3, y3, (x3 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #botton right
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)

        self.canvas.grid()
    
        self.start_button = Button(instructionFrame, text="Start Calibration",
                              command=self.start_blinking)
        self.stop_button = Button(instructionFrame, text="Exit",
                                                   command=self.stop_blinking)
        self.start_button.grid(column = 0)
        self.stop_button.grid(column = 1, row = 0)
    
        global calCircle
        calCircle = 1


    def start_blinking(self):
        self.do_blink = True
        self.blink()

    def stop_blinking(self):
        self.destroy()

    def blink(self):
        self.canvas.itemconfigure(self.oval1, fill="red")
        self.after(1000, self.blink2)

    def blink2(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal1.jpg",img) #save image
        self.canvas.itemconfigure(self.oval1, fill = "black")
        self.canvas.itemconfigure(self.oval2, fill="red")
        self.after(1000, self.blink3)

    def blink3(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal2.jpg",img) #save image
        self.canvas.itemconfigure(self.oval2, fill = "black")
        self.canvas.itemconfigure(self.oval3, fill="red")
        self.after(1000, self.blink4)

    def blink4(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal3.jpg",img) #save image
        self.canvas.itemconfigure(self.oval3, fill = "black")
        self.canvas.itemconfigure(self.oval4, fill="red")
        self.after(1000, self.blink5)

    def blink5(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal4.jpg",img) #save image
        self.canvas.itemconfigure(self.oval4, fill = "black")
        self.canvas.itemconfigure(self.oval5, fill="red")
        self.after(1000, self.blink6)

    def blink6(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal5.jpg",img) #save image
        self.canvas.itemconfigure(self.oval5, fill = "black")
        self.canvas.itemconfigure(self.oval6, fill="red")
        self.after(1000, self.blink7)

    def blink7(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal6.jpg",img) #save image
        self.canvas.itemconfigure(self.oval6, fill = "black")
        self.canvas.itemconfigure(self.oval7, fill="red")
        self.after(1000, self.blink8)

    def blink8(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal7.jpg",img) #save image
        self.canvas.itemconfigure(self.oval7, fill = "black")
        self.canvas.itemconfigure(self.oval8, fill="red")
        self.after(1000, self.blink9)

    def blink9(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal8.jpg",img) #save image
        self.canvas.itemconfigure(self.oval8, fill = "black")
        self.canvas.itemconfigure(self.oval9, fill="red")
        self.after(1000, self.blink10)

    def blink10(self):
        if s:    # frame captured without any errors
            cv2.imwrite("cal9.jpg",img) #save image
        self.canvas.itemconfigure(self.oval9, fill = "black")
        print "Config done"

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    root = MyApp()
    root.mainloop()