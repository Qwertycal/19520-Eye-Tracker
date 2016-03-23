import cv2
import Tkinter

import numpy as np

import time
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pyautogui

purple_thresh = 10
blue_thresh = 30
green_thresh = 50
amber_thresh = 70
red_thresh = 90

purple = "#191970"
blue = "#00b7ea"
green = "#0F0"
orange = "#FFA500"
red = "#F00"

screenwidth, screenheight = pyautogui.size()

img_heatmap = np.zeros((screenheight,screenwidth), np.uint8)
img_heatmap = np.array(img_heatmap)
    
img_display = np.ones((screenheight,screenwidth,3), np.uint8) * 255
img_display = np.array(img_display)


#def _create_circle(self, x, y, r, **kwargs):
#    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
#Tkinter.Canvas.create_circle = _create_circle


# This function updates the heatmap image values
def draw(row,column):
#    root.update()

    size = 11
    count = 1

    for a in range(0,(size*2)+1):
        for b in range(0,(size*2)+1):
            if column+b-size >= 0 and row+a-size >= 0 and column+b-size < screenheight and row+a-size <screenwidth:
                img_heatmap[column+b-size,row+a-size] = img_heatmap[column+b-size,row+a-size] + 1
                img_display[column+b-size,row+a-size] = img_colours[img_heatmap[column+b-size,row+a-size]]



#This function defines the colour threshold for heatmap
def heatmap_try1():

    img_colours = np.zeros((255,3), np.uint8)
    for i in range(0,255):
        if i == 0:
            val = (255,255,255) # white
            img_colours[i] = val
        elif i <= 5:
            val = (128,0,0) # dark blue
            img_colours[i] = val
        elif i > 5 and  i <= 10:
            val = (237,149,100) # light blue
            img_colours[i] = val
        elif i > 10 and i <= 20:
            val = (0,252,124) # green
            img_colours[i] = val
        elif i > 20 and i <= 30:
            val = (0,140,255) # orange
            img_colours[i] = val
        elif i > 30:
            val = (0,0,255) # red
            img_colours[i] = val

    return img_colours


# Can be used to generate heatmap providing a list of x and y coordinates values are available
def generateHeatmapList(coords2):

    global canvas
    global root
    global w
    global h
    global img_colours
    
    img_colours = heatmap_try1()


    for j in range(len(coords2)):
        val = coords2[j]
        coordsX = val[0]
        coordsY = val[1]
        
        coordsX = int(coordsX)
        coordsY = int(coordsY)
        draw(coordsX,coordsY)
        
        kernel = np.ones((20,20),np.float32)/400
        new_image = cv2.filter2D(img_display,-1,kernel)
        cv2.imshow('HeatMap',new_image)
        cv2.waitKey(1)


# Can be used to pass in individual X and Y coordinates therefore dynamically building up heatmap
def generateHeatmap(coordsX, coordsY):
    
    global canvas
    global root
    global w
    global h
    global img_colours

    img_colours = heatmap_try1()
    
        
    coordsX = float(coordsX)
    coordsY = float(coordsY)
    draw(coordsX,coordsY)
    
    kernel = np.ones((20,20),np.float32)/400
    new_image = cv2.filter2D(img_display,-1,kernel)
    cv2.imshow('HeatMap',new_image)
    cv2.waitKey(1)



def main():
    
    with open('pointsTest2.csv','rb') as file:
        contents = csv.reader(file)
        coords2 = list()
        for x in contents:
            coords2.append(x)

#    generateHeatmapList(coords2)

    for i in range(len(coords2)):
        val = coords2[i]
        coordsX = val[0]
        coordsY = val[1]
        generateHeatmap(coordsX,coordsY)


    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()



if __name__ == '__main__':
    main()