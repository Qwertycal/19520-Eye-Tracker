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

def move_mouse(x1,y1):
    spaceCount = 0
    cursorClick = 20 #alters how long the user must look at a point before a click
    maxMovement = 200 #alters the area the user must look at to invoke a click
    
    #Move to the first location and add the location to the list
    if len(pointsVisited) <=0:
        pyautogui.moveTo((x1,y1), duration=0)
        pointsVisited.append(pyautogui.position())
    
    #For the next locations find the previous location, work out the distance between the previous
    #location and the one to move to and set the time this should take
    #Move to the current location for the set amount of time, and add the current location to the list
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
        spaceCount = 0
        #For all the moves between the (cursorClick)th previous move and the current one,
        #check if the cursor has stayed within the bounds, if it has for each then add one to spaceCount
        for j in range((prevPos-(cursorClick - 1)), (prevPos+1)):
            if((lowBound1<= pointsVisited[j][0] <= highBound1) & (lowBound2) <= pointsVisited[j][1] <= (highBound2)):
                spaceCount += 1
            else:
                spaceCount = 0
            print spaceCount
    #If there have been (cursorClick) consecutive moves in a row within the bounds, then click, and check if there should be a scroll
    if (spaceCount == cursorClick):
        print('Click')
        pyautogui.click()
        spaceCount = 0

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






