import pyautogui
import math

pyautogui.FAILSAFE = False
speed = 1410
spaceCount = 0
cursorClick = 100
maxMovement = 10
cursorDoubleClick = 1000
doubleCount = 0
width, height = pyautogui.size() #get the width and height of the screen

#List of coordinates to move to
coords = [(0,0), (492, 383)]
pointsVisited = []
pyautogui.moveTo(coords[0], duration=0.25)

var = 1
loop = 1

while var == 1:
    #print (var)
	pointsVisited.append(pyautogui.position())
    #print (pointsVisited)
	if (loop == 1):
		for i in range (1, len(coords)):
			#For each set of coordinates in the list, move to the coordinates, at an appropriate speed.
			distance = math.sqrt(math.pow((coords[i][0])-(coords[i-1][0]), 2) + math.pow((coords[i][1]) -(coords[i-1][1]),2))
			dur = distance/speed
			print(dur)
			pyautogui.moveTo(coords[i], duration=dur); print (pyautogui.position()[0]); print (pyautogui.position()[1])
			pointsVisited.append(pyautogui.position())
			loop += 1
	# else:
		# pointsVisited.append(pyautogui.position())
    #If the cursor has been in the same sort of location for a while, then click
	if len(pointsVisited) > cursorClick:
		prevPos = len(pointsVisited) - 1
        #Look at the last 4th previous move, set a box, 10 pixels wide around the cursors location at this move.
		lowBound1 = (pointsVisited[prevPos-cursorClick][0])-maxMovement
		lowBound2 = (pointsVisited[prevPos-cursorClick][1])-maxMovement
		highBound1 = (pointsVisited[prevPos-cursorClick][0])+maxMovement
		highBound2 = (pointsVisited[prevPos-cursorClick][1])+maxMovement
		spaceCount = 0
		
        #For all the moves between the 4th previous move and the current one, check if the cursor has stayed within the bounds, if it has for each then add one to spaceCount
		for j in range((prevPos-(cursorClick - 1)), (prevPos+1)):
            #print ('j' + str(j))
            #print('spaceCount: ' + str(spaceCount))
			if((lowBound1<= pointsVisited[j][0]) & (pointsVisited[j][0] <= highBound1) & 
			(lowBound2) <= pointsVisited[j][1]) & (pointsVisited[j][1] <= (highBound2)):
				spaceCount += 1
			else:
				spaceCount = 0
    #If there have been 4 consecutive moves in a row within the bounds, then click, and check if there should be a scroll
	if (spaceCount == cursorClick):
		print('Click')
		pyautogui.click()
		spaceCount = 0
		#If the cursor is near a scroll bar, then scroll, up or down
		scrollUpLoc = []
		scrollUpLoc.append(pyautogui.locateAllOnScreen('scrollUpWindows.png', grayscale=True))
		scrollUpLoc.append(pyautogui.locateAllOnScreen('scrollUpWindowsHighlighted.png', grayscale=True))
		#print('scrollUpLoc' + str(scrollUpLoc[0]))
		print (list(pyautogui.locateAllOnScreen('scrollUpWindowsHighlighted.png', grayscale=True)))
		print (list(pyautogui.locateAllOnScreen('scrollUpWindows.png', grayscale=True)))
		scrollDownLoc = []
		scrollDownLoc.append(pyautogui.locateAllOnScreen('scrollDownWindows.png', grayscale=True))
		scrollDownLoc.append(pyautogui.locateAllOnScreen('scrollDownWindowsHighlighted.png', grayscale=True))
		#print('scrollDownLoc' + str(scrollDownLoc[0]))
		list(scrollUpLoc)
		x, y = pyautogui.position()
		print (x, y)
		for k in (pyautogui.locateAllOnScreen('scrollUpWindowsHighlighted.png', grayscale=True)):
			print 'Found up bar'
			# if hasattr(scrollUpLoc[k], '__getitem__'):
				# print ('has attr up')
			if (x > (k[0] - 10) and x < (k[0] + k[2] + 10) and 
			y > (k[1] - 10) and y < (k[1] + k[3] + 10)):
				print ("Implement scroll up")
				pyautogui.scroll(5)
				print("Scrolled up")
		#for l in scrollDownLoc:
			#print l
			# if hasattr(scrollDownLoc[k], '__getitem__'):
				# print ('hasattr down')
				# if (x > (scrollDownLoc[l][0] - 10) and x < (scrollDownLoc[l][0] + scrollDownLoc[l][2] + 10) and 
				# y > (scrollDownLoc[l][1] - 10) and y < (scrollDownLoc[l][1] - scrollDownLoc[l][3] + 10)):
					# print ("Implement scroll down")
					# pyautogui.scroll(5)
					# print("Scrolled down")
	i += 1






