import pyautogui
import math
import cv2
import csv
import sys

pyautogui.FAILSAFE = False
speed = 1500 #Controls the speed of the mouse

width, height = pyautogui.size() #get the width and height of the screen
pointsVisited = [] #
#pointsClicked = []

global scrollDownFile
global scrollUpFile
global scrollDownFileHighlighted
global scrollUpFileHightlighted
global scrollDist

if (sys.platform == 'win32'):
	scrollUpFile = 'scrollUpWindows.png'
	scrollDownFile = 'scrollDownWindows.png'
	scrollUpFileHightlighted = 'scrollUpWindowsBlue.png'
	scrollDownFileHighlighted = 'scrollDownWindowsBlue.png'
	scrollDist = 200
elif (sys.platform == 'darwin'):
    scrollUpFile = 'scrollUpMac.png'
    scrollDownFile = 'scrollDownMac.png'
    scrollUpFileHightlighted = 'scrollUpMacHighlighted.png'
    scrollDownFileHighlighted = 'scrollDownMacHighlighted.png'
    scrollDist = 20

def move_mouse(x1,y1):
	spaceCount = 0
	cursorClick = 10 #alters how long the user must look at a point before a click
	maxMovement = 250 #alters the area the user must look at to invoke a click
	#maxClickMovement = 200
	cursorDoubleClick = 20
	doubleCount = 0
	scollBox = 50
	
	
	#Move to the first location and add the location to the list	
	if len(pointsVisited) <=0:
		pyautogui.moveTo((x1,y1), duration=0)
		pointsVisited.append(pyautogui.position())
    
    #For the next locations find the previous location, work out the distance between
    #the previous location and the one to move to and set the time this should take
    #Move to the current location for the set amount of time, and add the current
    #location to the list
	else:
		prevPos = len(pointsVisited) - 1
		point = pointsVisited[prevPos]
		oldX = point[0]
		oldY = point[1]
		#For each set of coordinates in the list, move to the coordinates, at an appropriate speed.
		distance = math.sqrt(math.pow(x1-oldX, 2) + math.pow(y1 -oldY,2))
		dur = distance/speed
		pyautogui.moveTo((x1,y1), duration=dur)
		pointsVisited.append(pyautogui.position())

#    print 'len points visited'
#    print (len(pointsVisited))
    #If there have been x number of movements set a bounding box around the first location in the range of x
    #Check each of the locaitons in this range, if all of them are within the bounding box, invoke a click
	if len(pointsVisited) > cursorClick:
		#Look at the first location in the range (cursorClick) set a box, (maxMovement) pixels wide around
		#the cursors location at this point.
		lowBound1 = (pointsVisited[prevPos-cursorClick][0])-maxMovement
		lowBound2 = (pointsVisited[prevPos-cursorClick][1])-maxMovement
		highBound1 = (pointsVisited[prevPos-cursorClick][0])+maxMovement
		highBound2 = (pointsVisited[prevPos-cursorClick][1])+maxMovement
		#spaceCount = 0
		#For all the moves between the (cursorClick)th previous move and the current one,
		#check if the cursor has stayed within the bounds, if it has for each then add one to spaceCount
		for j in range((prevPos-(cursorClick - 1)), (prevPos+1)):
			if((lowBound1<= pointsVisited[j][0]) & (pointsVisited[j][0] <= highBound1) & 
			(lowBound2 <= pointsVisited[j][1]) & (pointsVisited[j][1] <= highBound2)):
				spaceCount += 1
			else:
				spaceCount = 0
		if len(pointsVisited) > cursorDoubleClick:
			for k in range((prevPos-(cursorDoubleClick - 1)), (prevPos+1)):
				if((lowBound1<= pointsVisited[k][0]) &  (pointsVisited[k][0] <= highBound1) & 
				(lowBound2 <= pointsVisited[k][1]) & (pointsVisited[k][1] <= highBound2)):
					doubleCount += 1
				else:
					doubleCount = 0
	#print doubleCount
	#print spaceCount
	#If there have been (cursorClick) consecutive moves in a row within the bounds, then click, and check if there should be a scroll
	if (doubleCount == cursorDoubleClick):
		print ('Double Click')
		pyautogui.click(clicks = 2)
		doubleCount = 0
		spaceCount = 0

	if (spaceCount == cursorClick):
		print('Click Invoked')
		#if len(pointsClicked) <= cursorDoubleClick:
		pyautogui.click()
		#pointsClicked.append(pyautogui.position())
		spaceCount = 0
						
		for k in (pyautogui.locateAllOnScreen(scrollUpFileHightlighted, grayscale=True)):
			if (x1 > (k[0] - scollBox) and x1 < (k[0] + k[2] + scollBox) and y1 > (k[1] - scollBox) and y1 < (k[1] + k[3] + scollBox)):
				pyautogui.scroll(scrollDist)
				print("Scrolled Up")
		for l in (pyautogui.locateAllOnScreen(scrollDownFileHighlighted, grayscale=True)):
			if (x1 > (l[0] - scollBox) and x1 < (l[0] + l[2] + scollBox) and y1 > (l[1] - scollBox) and y1 < (l[1] + l[3] + scollBox)):
				pyautogui.scroll(-scrollDist)
				print("Scrolled Down")
		for m in (pyautogui.locateAllOnScreen(scrollUpFile, grayscale=True)):
			if (x1 > (m[0] - scollBox) and x1 < (m[0] + m[2] + scollBox) and y1 > (m[1] - scollBox) and y1 < (m[1] + m[3] + scollBox)):
				pyautogui.scroll(scrollDist)
				print("Scrolled Up")
		for n in (pyautogui.locateAllOnScreen(scrollDownFile, grayscale=True)):
			if (x1 > (n[0] - scollBox) and x1 < (n[0] + n[2] + scollBox) and y1 > (n[1] - scollBox) and y1 < (n[1] + n[3] + scollBox)):
				pyautogui.scroll(-scrollDist)
				print("Scrolled Down")
	