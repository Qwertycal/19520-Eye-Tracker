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

#def _create_circle(self, x, y, r, **kwargs):
#    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
#Tkinter.Canvas.create_circle = _create_circle

def draw(row,column):
#    root.update()

    size = 7
    count = 1

    for a in range(0,(size*2)+1):
        for b in range(0,(size*2)+1):
            img_heatmap[row+a-size,column+b-size] = img_heatmap[row+a-size,column+b-size] + 1
#            print "%d: row: %d  column: %d  val: %d" % (  count, row+a-size, column+b-size,img_heatmap[row+a-size,column+b-size])
#            count = count+1


#    print img_heatmap
#    print img_heatmap.shape

#    threshed = cv2.adaptiveThreshold(img_heatmap, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)

#    cv2.imshow('image', threshed)
#    time.sleep(0.01)
#    hist2d(img_heatmap,bins=100);

    #now just plug the data into pcolormesh, it's that easy!
#    heatmap = plt.pcolor(img_heatmap, cmap=plt.cm.Blues, alpha=0.8)
#    plt.pcolormesh(screenwidth, screenheight, img_heatmap)
#    plt.show()

#    for x in range(0,(size*2)+1):
#        for y in range(0,(size*2)+1):
#            val = img_heatmap[row+x-size,column+y-size]
#            if img_heatmap[row+x-size,column+y-size] < purple_thresh:
##                canvas.create_circle(row-size+x, column-size+y, 3, fill=purple, outline=purple)
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill=purple,outline=purple)
#        
#            elif img_heatmap[row+x-size,column+y-size] >= purple_thresh and img_heatmap[row+x-size,column+y-size] < blue_thresh:
##                canvas.create_circle(row-size+x, column-size+y, 3, fill=blue, outline=blue)
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill=blue,outline=blue)
#            
#            elif img_heatmap[row+x-size,column+y-size] >= blue_thresh and img_heatmap[row+x-size,column+y-size] < green_thresh:
#
##                canvas.create_circle(row-size+x, column-size+y, 3, fill=green, outline=green)
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill=green,outline=green)
#            
#            elif img_heatmap[row-size+x,column-size+y] >= green_thresh and img_heatmap[row-size+x,column-size+y] < amber_thresh:
#
##                canvas.create_circle(row-size+x, column-size+y, 3, fill=orange, outline=orange)
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill=orange,outline=orange)
#            else:
##                canvas.create_circle(row-size+x, column-size+y, 3, fill=red, outline=red)
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill=red,outline=red)
#
#    root.update()
#                canvas.create_rectangle(row-size+x,column-size+y,row+x-size+1,column+y-size+1,fill="#F00",outline="#F00")


def draw_start_end(x1,y1,x2,y2):



    # create two lists of stepped x and y
    xinc = (x2 - x1)/50
    yinc = (y2 - y1)/50
    #     print xinc, yinc
    
    xlist = []
    
#    print xinc
#    print yinc

    for x in xrange(x1, x2+xinc, xinc):
        #         print x
        xlist.append(x)
    
    ylist = []

    for y in xrange(y1, y2+yinc, yinc):
        #         print y
        ylist.append(y)




#if xinc == 0:
#    xinc = 1/100
#        #        print xinc
#        for x in xrange(x1, x2+xinc, 1):
#            #         print x
#            xlist.append(x1)
#    else:
#        for x in xrange(x1, x2+xinc, xinc):
#            #         print x
#            xlist.append(x)
#
#ylist = []
#    
#    if yinc == 0:
#        for y in xrange(y1, y2+yinc, 1):
#            #         print y
#            ylist.append(y1)
#else:
#    for y in xrange(y1, y2+yinc, yinc):
#        #         print y
#        ylist.append(y)


    for j in range(len(xlist)):
        print "%d %d" % (xlist[j],ylist[j])
        draw(xlist[j],ylist[j])


def main():
    
    global img_heatmap
    global canvas
    global root
    global w
    global h
    
    with open('points2.csv','rb') as file:
        contents = csv.reader(file)
        coords2 = list()
        for x in contents:
            coords2.append(x)

#    root = Tk()
#    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#
#    root.geometry("%dx%d" % (w,h))

    #setup the 2D grid with Numpy
#    x, y = np.meshgrid(screenwidth, screenheight)

    img_heatmap = np.zeros((screenwidth,screenheight), np.uint8)
#    img_heatmap[row,column] = 1

#    convert intensity (list of lists) to a numpy array for plotting
#    img_heatmap = np.array(img_heatmap)

#    canvas = Canvas()
#    canvas.pack(fill=BOTH, expand=1)

#    draw_start_end(50,50,700,400)
#    for j in range(0,50):
#        draw(100,100)
#        draw(150,150)
#        draw(200,200)

    for j in range(len(coords2)):
        val = coords2[j]
        coordsX = val[0]
        coordsY = val[1]
        
        coordsX = int(coordsX)
        coordsY = int(coordsY)
        draw(coordsX,coordsY)

    cv2.imwrite('color_img.jpg', img_heatmap)
    image = cv2.imread('color_img.jpg', 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray)

    blur = cv2.GaussianBlur(image,(5,5),0)
    cv2.imshow('image after blur',blur)

    new_image = image.copy()

    cv2.circle(new_image, (150,150), 65, (255,255,255),-1)
    cv2.circle(new_image, (300,300), 65, (255,255,255),-1)
    cv2.circle(new_image, (300,100), 65, (255,255,255),-1)
    cv2.imshow('new_image',new_image)

    gray = new_image.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)



    #Just making sure everything is binary
#    threshold(mSource_Gray,mSource_Gray,254,255,THRESH_BINARY);
    (T, thresh) = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
#    cv2.imshow('image thresh',thresh)

    output = None
    mBlobDist = None
    mBlobHeatmap = None
    mHeatmap = None
    mBlobMask = np.zeros((screenwidth,screenheight), np.uint8)

    mDist = cv2.distanceTransform(gray,cv2.DIST_L2, 3)
    cv2.imshow('image mDist 1',mDist)
    print mDist
    mDist = cv2.normalize(mDist,0,1.,cv2.NORM_MINMAX)
    print mDist

    mDist = np.uint8(mDist)
    mDist = mDist * 255
    print mDist
    cv2.imshow('image mDist 2',mDist)

#    output = cv2.convertTo(output,CV_8UC1,255,0);
    cvuint8 = cv2.convertScaleAbs(image)
    print cvuint8.dtype

#    cv2.imshow('output',cvuint8)

    _,contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:3]
    print len(cnts)


#    mBlobMask = cv2.cvtColor(mBlobMask, cv2.COLOR_GRAY2BGR)
    for c in cnts:
        #draw pupil circumference
        cv2.drawContours(mBlobMask,c,-1,(255,255,255),-1)
#        mBlobDist = cv2.bitwise_and(mDist,mDist,mask = mBlobMask)
#        mBlobHeatmap = cv2.applyColorMap(mBlobDist,cv2.COLORMAP_JET)
#        mBlobHeatmap = cv2.GaussianBlur(mBlobHeatmap,(21,21),0)
#        mHeatmap = cv2.bitwise_and(mBlobHeatmap,mBlobHeatmap, mask = mBlobMask)


    cv2.imshow('image mBlobMask',mBlobMask)
#    cv2.imshow('image mBlobDist',mBlobDist)
#    cv2.imshow('image mBlobHeatmap',mBlobHeatmap)
#    cv2.imshow('image heatmap',mHeatmap)



    print "End"

#    data = [
#        go.Heatmap(
#           z=img_heatmap
#           )
#        ]
#    plot_url = plotly.offline.plot(data, filename='basic-heatmap')


#    root.mainloop()

    while(1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()



if __name__ == '__main__':
    main()