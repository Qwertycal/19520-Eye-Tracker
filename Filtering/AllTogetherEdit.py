import pyautogui
import math
import cv2
import csv
#
#with open('points2.csv','rb') as file:
#    contents = csv.reader(file)
#    coords = list()
#    for x in contents:
#        coords.append(x)


pyautogui.FAILSAFE = False
speed = 1500 #Controls the speed of the mouse
#global spaceCount
#spaceCount = 0
#cursorClick = 4
#maxMovement = 500

width, height = pyautogui.size() #get the width and height of the screen
pointsVisited = []
pointsClicked = []

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
#        print doubleCount
	print spaceCount
	#If there have been (cursorClick) consecutive moves in a row within the bounds, then click, and check if there should be a scroll
	if (doubleCount == cursorDoubleClick):
		print 'double click'
		pyautogui.click(clicks = 2)
		doubleCount = 0
		spaceCount = 0

	if (spaceCount == cursorClick):
		print('Click Invoked')
		#if len(pointsClicked) <= cursorDoubleClick:
		pyautogui.click()
		pointsClicked.append(pyautogui.position())
		spaceCount = 0
						
		for k in (pyautogui.locateAllOnScreen('scrollUpWindowsBlue.png', grayscale=True)):
			if (x1 > (k[0] - scollBox) and x1 < (k[0] + k[2] + scollBox) and y1 > (k[1] - scollBox) and y1 < (k[1] + k[3] + scollBox)):
				pyautogui.scroll(200)
				print("Scrolled up")
		for l in (pyautogui.locateAllOnScreen('scrollDownWindowsBlue.png', grayscale=True)):
			if (x1 > (l[0] - scollBox) and x1 < (l[0] + l[2] + scollBox) and y1 > (l[1] - scollBox) and y1 < (l[1] + l[3] + scollBox)):
				pyautogui.scroll(-200)
				print("Scrolled down")
		for m in (pyautogui.locateAllOnScreen('scrollUpWindows.png', grayscale=True)):
			if (x1 > (m[0] - scollBox) and x1 < (m[0] + m[2] + scollBox) and y1 > (m[1] - scollBox) and y1 < (m[1] + m[3] + scollBox)):
				pyautogui.scroll(200)
				print("Scrolled up")
		for n in (pyautogui.locateAllOnScreen('scrollDownWindows.png', grayscale=True)):
			if (x1 > (n[0] - scollBox) and x1 < (n[0] + n[2] + scollBox) and y1 > (n[1] - scollBox) and y1 < (n[1] + n[3] + scollBox)):
				pyautogui.scroll(-200)
				print("Scrolled down")
				
		# for o in (pyautogui.locateAllOnScreen('scrollUpWordHighlighted.png', grayscale=True)):
			# if (x1 > (o[0] - scollBox) and x1 < (o[0] + o[2] + scollBox) and y1 > (o[1] - scollBox) and y1 < (o[1] + o[3] + scollBox)):
				# pyautogui.scroll(200)
				# print("Scrolled up")
		# for p in (pyautogui.locateAllOnScreen('scrollDownWordHighlighted.png', grayscale=True)):
			# if (x1 > (p[0] - scollBox) and x1 < (p[0] + p[2] + scollBox) and y1 > (p[1] - scollBox) and y1 < (p[1] + p[3] + scollBox)):
				# pyautogui.scroll(-200)
				# print("Scrolled down")
		# for q in (pyautogui.locateAllOnScreen('scrollUpWord.png', grayscale=True)):
			# if (x1 > (q[0] - scollBox) and x1 < (q[0] + q[2] + scollBox) and y1 > (q[1] - scollBox) and y1 < (q[1] + q[3] + scollBox)):
				# pyautogui.scroll(200)
				# print("Scrolled up")
		# for r in (pyautogui.locateAllOnScreen('scrollDownWord.png', grayscale=True)):
			# if (x1 > (r[0] - scollBox) and x1 < (r[0] + r[2] + scollBox) and y1 > (r[1] - scollBox) and y1 < (r[1] + r[3] + scollBox)):
				# pyautogui.scroll(-200)
				# print("Scrolled down")
#        print 'Point Clicked'
#        print pointsClicked[0][0]
#        print pointsClicked[0][1]
#        else:
#            prevClickPos = len(pointsClicked) - 1
#            #print prevClickPos
#            for k in range ((prevClickPos - cursorDoubleClick), prevClickPos):
#                lowClickBound1 = (pointsClicked[prevClickPos - cursorDoubleClick][0])-maxClickMovement
#                lowClickBound2 = (pointsClicked[prevClickPos - cursorDoubleClick][1])-maxClickMovement
#                highClickBound1 = (pointsClicked[prevClickPos - cursorDoubleClick][0])+maxClickMovement
#                highClickBound2 = (pointsClicked[prevClickPos - cursorDoubleClick][1])+maxClickMovement
#        
#
#                if(lowClickBound1 <= pyautogui.position()[0] <= highClickBound1 & lowClickBound2 <= pyautogui.position()[1] <= highClickBound2):
#                    pyautogui.moveTo(pointsClicked[prevClickPos][0],pointsClicked[prevClickPos][1])
#                    print 'double click'
#                    pyautogui.click(clicks = 2)
#
#            pyautogui.click()
#            pointsClicked.append(pyautogui.position())
#            spaceCount = 0
#    
#            print 'Point Clicked'
#            print pointsClicked[prevClickPos][0]
#            print pointsClicked[prevClickPos][1]

    



#def stuff():
#    #List of coordinates to move to
#    #coords = [(0,0), (800, 800),(90, 110), (103, 104), (98, 97), (102, 104)]
#    pointsVisited = []
#    pyautogui.moveTo(coords[0], duration=0.25)
#
#    var = 1
#    loop = 1
#
#    while var == 1:
#        #print (var)
#        pointsVisited.append(pyautogui.position())
#        #print (pointsVisited)
#        if (loop == 1):
#            for i in range (1, len(coords)):
#                #For each set of coordinates in the list, move to the coordinates, at an appropriate speed.
#                distance = math.sqrt(math.pow((int(coords[i][0]))-(int(coords[i-1][0])), 2) + math.pow((int(coords[i][1])) -(int(coords[i-1][1])),2))
#                dur = distance/speed
#                print(dur)
#                pyautogui.moveTo(coords[i], duration=dur)
#                pointsVisited.append(pyautogui.position())
#                loop += 1
#        
#        #If the cursor has been in the same sort of location for a while, then click
#        if (i>(cursorClick - 1)):
#            #Look at the last 4th previous move, set a box, 10 pixels wide around the cursors location at this move.
#            lowBound1 = (pointsVisited[i-cursorClick][0])-maxMovement
#            lowBound2 = (pointsVisited[i-cursorClick][1])-maxMovement
#            highBound1 = (pointsVisited[i-cursorClick][0])+maxMovement
#            highBound2 = (pointsVisited[i-cursorClick][1])+maxMovement
#            spaceCount = 0
#            
#            #For all the moves between the 4th previous move and the current one, check if the cursor has stayed within the bounds, if it has for each then add one to spaceCount
#            for j in range((i-(cursorClick - 1)), (i+1)):
#                #print ('j' + str(j))
#                #print('spaceCount: ' + str(spaceCount))
#                if((lowBound1<= pointsVisited[j][0] <= highBound1) & (lowBound2) <= pointsVisited[j][1] <= (highBound2)):
#                    spaceCount += 1
#                else:
#                    spaceCount = 0
#        #If there have been 4 consecutive moves in a row within the bounds, then click, and check if there should be a scroll
#        if (spaceCount == cursorClick):
#            print('Click')
#            pyautogui.click()
#            spaceCount = 0
#            #If the cursor is near a scroll bar, then scroll, up or down
#            scrollUpLoc = pyautogui.locateOnScreen('scrollUp.png')
#            print('scrollUpLoc' + str(scrollUpLoc))
#            scrollDownLoc = pyautogui.locateOnScreen('scrollDown.png')
#            print('scrollDownLoc' + str(scrollDownLoc))
#            x, y = pyautogui.position()
#            if (scrollUpLoc != None):
#                if (x > (scrollUpLoc[0] - 5) and x < (scrollUpLoc[0] + scrollUpLoc[2] + 5) and y > (scrollUpLoc[1] - 5) and y < (scrollUpLoc[1] + scrollUpLoc [3] + 5)):
#                    print ("Implement scroll up")
#                    pyautogui.scroll(5)
#                    print("Scrolled up")
#            if (scrollDownLoc != None):
#                if (x > (scrollDownLoc[0] - 5) and x < (scrollDownLoc[0] + scrollDownLoc[2] + 5) and y > (scrollDownLoc[1] - 5) and y < (scrollDownLoc[1] + scrollDownLoc [3] + 5)):
#                    print ("Implement scroll down")
#                    pyautogui.scroll(5)
#                    print("Scrolled down")
#        i += 1