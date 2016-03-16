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
#    width, height = pyautogui.size() #get the width and height of the screen
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    print(width)
    print(height)
    
    global qWidth
    qWidth = width/4
    global tHeight
    tHeight = height/3
    
    dotSize = 26
    x1 = (numpy.mean([0, qWidth]) - (dotSize/2))
    y1 = (numpy.mean([0,tHeight]) - (dotSize/2))
    x2 = x1 + qWidth
    x3 = x2 + qWidth
    x4 = x3 + qWidth
    x5 = width/2
    
    y2 = y1 + tHeight
    y3 = y2 +tHeight
    y4 = ((y2 - y1)/2) + y1
    y5 = ((y2 - y1)/2) + y2
    
#    canvasFrame = Frame(root, bg = "red", width = width, height = (height - 100))
    instructionFrame = Frame(root, width = width, bg = "red", height = 50)
    canvas = Canvas(root, width = width, height = (height - 100))
    canvas.create_oval(x1, y1, (x1 + dotSize), (y1 + dotSize), outline = "black", fill = "black") #top left
    canvas.create_oval(x4, y1, (x4 + dotSize), (y1 + dotSize), outline = "black", fill = "black") #top right
    
    canvas.create_oval(x2, y4, (x2 + dotSize), (y4 + dotSize), outline = "black", fill = "black") #top left
    canvas.create_oval(x3, y4, (x3 + dotSize), (y4 + dotSize), outline = "black", fill = "black") #top right
    
    canvas.create_oval(x1, y2, (x1 + dotSize), (y2 + dotSize), outline = "black", fill = "black") #middle left
    canvas.create_oval(x4, y2, (x4 + dotSize), (y2 + dotSize), outline = "black", fill = "black") #middle right
    
    canvas.create_oval(x2, y5, (x2 + dotSize), (y5 + dotSize), outline = "black", fill = "black") #top left
    canvas.create_oval(x3, y5, (x3 + dotSize), (y5 + dotSize), outline = "black", fill = "black") #top right

    canvas.create_oval(x1, y3, (x1 + dotSize), (y3 + dotSize), outline = "black", fill = "black") #bottom left
    canvas.create_oval(x4, y3, (x4 + dotSize), (y3 + dotSize), outline = "black", fill = "black") #botton right

    submitButton = Button(instructionFrame, text = "Submit", command = moveMouse)

#    canvasFrame.grid()
    canvas.grid(sticky = W)
    instructionFrame.grid(row = 1)
    submitButton.grid()
    
    
def moveMouse():
    screenLocX1 = qWidth/2
    screenLocX2 = screenLocX1 +qWidth
    screenLocX3 = screenLocX2 + qWidth
    screenLocX4 = screenLocX3 + qWidth
    
    screenLocY1 = tHeight/2
    screenLocY2 = screenLocY1 + (tHeight/2)
    screenLocY3 = screenLocY2 + (tHeight/2)
    screenLocY4 = screenLocY3 + (tHeight/2)
    screenLocY5 = screenLocY4 + (tHeight/2)
    
    dur = 0.4
    coords = [(screenLocX1, screenLocY1), (screenLocX2, screenLocY2), (screenLocX3, screenLocY2), (screenLocX4, screenLocY1),
              (screenLocX1, screenLocY3), (screenLocX2, screenLocY4), (screenLocX3, screenLocY4), (screenLocX4, screenLocY3),
              (screenLocX1, screenLocY5), (screenLocX4, screenLocY5)]
            
    for i in range (0, len(coords)):
        pyautogui.moveTo(coords[i], duration=dur)

screenSetup()
root.mainloop()