from Tkinter import *
import pyautogui
import numpy

from PIL import Image, ImageDraw

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.overrideredirect(True)
        master.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        master.focus_set()  # <-- move focus to this widget
        master.bind('<Escape>',lambda e: root.quit())


root=Tk()
app=FullScreenApp(root)

def submit():
    print "Submit button pressed"

def screenSetup():
    width, height = pyautogui.size() #get the width and height of the screen
    print(width)
    print(height)
    
    global qWidth
    global tHeight
    global q3Width
    qWidth = width/4
    q3Width = width/3
    tHeight = height/3
    
    dotSize = 26
    x1 = (numpy.mean([0, qWidth]) - (dotSize/2))
    y1 = (numpy.mean([0,tHeight]) - (dotSize/2))
    x2 = x1 + qWidth
    x3 = x2 + (qWidth/2)
    x4 = x2 + qWidth
    x5 = x4 + qWidth
    
    y2 = y1 + tHeight
    y3 = y2 +tHeight
    
    canvasFrame = Frame(root, bg = "red", width = width, height = (height - 100))
    instructionFrame = Frame(root, width = width, bg = "red", height = 50)
    canvas = Canvas(canvasFrame, width = width, height = (height - 100))
    canvas.create_oval(x1, y1, (x1 + dotSize), (y1 + dotSize), outline = "gray", fill = "gray") #top left
    canvas.create_oval(x3, y1, (x3 + dotSize), (y1 + dotSize), outline = "gray", fill = "gray") #top middle
    canvas.create_oval(x5, y1, (x5 + dotSize), (y1 + dotSize), outline = "gray", fill = "gray") #top right
    
    canvas.create_oval(x1, y2, (x1 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle left
    canvas.create_oval(x2, y2, (x2 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle second left
    canvas.create_oval(x4, y2, (x4 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle third left
    canvas.create_oval(x5, y2, (x5 + dotSize), (y2 + dotSize), outline = "gray", fill = "gray") #middle right

    canvas.create_oval(x1, y3, (x1 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #bottom left
    canvas.create_oval(x3, y3, (x3 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #bottom middle
    canvas.create_oval(x5, y3, (x5 + dotSize), (y3 + dotSize), outline = "gray", fill = "gray") #botton right

    submitButton = Button(instructionFrame, text = "Submit", command = moveMouse)

    canvasFrame.grid()
    canvas.grid(sticky = W)
    instructionFrame.grid(row = 1)
    submitButton.grid()

def moveMouse():
    screenLocX1 = qWidth/2
    screenLocX2 = screenLocX1 + qWidth
    screenLocX3 = screenLocX2 + (qWidth/2)
    screenLocX4 = screenLocX2 + qWidth
    screenLocX5 = screenLocX4 + qWidth
    
    screenLocY1 = tHeight/2
    screenLocY2 = screenLocY1 + tHeight
    screenLocY3 = screenLocY2 + tHeight
    
    dur = 0.4
    coords = [(screenLocX1, screenLocY1), (screenLocX3, screenLocY1), (screenLocX5, screenLocY1), (screenLocX1, screenLocY2),
              (screenLocX2, screenLocY2), (screenLocX4, screenLocY2), (screenLocX5, screenLocY2), (screenLocX1, screenLocY3),
              (screenLocX3, screenLocY3), (screenLocX5, screenLocY3)]
        
    for i in range (0, len(coords)):
        pyautogui.moveTo(coords[i], duration=dur)


screenSetup()
root.mainloop()