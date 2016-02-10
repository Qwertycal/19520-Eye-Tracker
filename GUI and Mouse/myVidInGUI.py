from Tkinter import *
import cv2
from PIL import Image, ImageTk

width, height = 302, 270
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.title("Testing Mode")
root.bind('<Escape>', lambda e: root.quit())

#Create Frame
mainFrame = Frame(root)

devViewFrame = Frame(mainFrame, bg = "blue", width = 300, height = 650)
userViewFrame = Frame(mainFrame, bg = "red", width = 500, height = 650)
videoFrame = Frame(devViewFrame, bg = "green", width = width, height = height)
coordsFrame = Frame(devViewFrame, bg = "black", width = 300, height = 380)
devButtonFrame = Frame(devViewFrame, width = 200)
userButtonFrame = Frame(userViewFrame, width = 500)
desktopViewFrame = Frame(userViewFrame, bg = "red", width = 500, height = 650)

#Create Buttons
mode = IntVar()
devModeB = Radiobutton(devButtonFrame,text="Developer Mode",variable=mode,value=1)
userModeB = Radiobutton(devButtonFrame,text="User Mode",variable=mode,value=2)
recordB = Button(userButtonFrame, text = "Record")
stopB = Button(userButtonFrame, text = "Stop")

#for Text width is mesaured in the number of characters, height is the number of lines displayed
outputCoOrds = Text(coordsFrame, width = 42, height = 20)
videoStream = Label(videoFrame)

#Put all of the elements into the GUI
mainFrame.grid(row = 1, column =0, sticky = N)
devViewFrame.grid(row = 1, column = 0, rowspan = 4, sticky = N)
userViewFrame.grid(row = 1, column = 3, sticky = N)
videoFrame.grid(row = 1, column = 0, sticky = N)
coordsFrame.grid(row = 2, column =0, sticky = NW)
devButtonFrame.grid(row = 0, column = 0, sticky = N)
userButtonFrame.grid(row = 0, column = 0, sticky = N)
desktopViewFrame.grid(row = 1, column = 0, sticky = N)

devModeB.grid (row = 0, column =0)
userModeB.grid (row = 0, column = 1)
recordB.grid (row = 0, column = 0)
stopB.grid (row = 0, column = 1)
outputCoOrds.grid(row = 0, column = 0, sticky = NW)
videoStream.grid()

#Show frame
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    videoStream.imgtk = imgtk
    videoStream.configure(image=imgtk)
    videoStream.after(10, show_frame)

show_frame()
root.mainloop()