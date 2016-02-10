import pyautogui
import math

pyautogui.FAILSAFE = False
speed = 1410
spaceCount = 0
cursorClick = 500
maxMovement = 10

width, height = pyautogui.size() #get the width and height of the screen

#List of coordinates to move to
coords = [(0,0), (800, 800),(90, 110), (103, 104), (98, 97), (102, 104)]
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
            pyautogui.moveTo(coords[i], duration=dur)
            pointsVisited.append(pyautogui.position())
            loop += 1
    
    #If the cursor has been in the same sort of location for a while, then click
    if (i>(cursorClick - 1)):
        #Look at the last 4th previous move, set a box, 10 pixels wide around the cursors location at this move.
        lowBound1 = (pointsVisited[i-cursorClick][0])-maxMovement
        lowBound2 = (pointsVisited[i-cursorClick][1])-maxMovement
        highBound1 = (pointsVisited[i-cursorClick][0])+maxMovement
        highBound2 = (pointsVisited[i-cursorClick][1])+maxMovement
        spaceCount = 0
        
        #For all the moves between the 4th previous move and the current one, check if the cursor has stayed within the bounds, if it has for each then add one to spaceCount
        for j in range((i-(cursorClick - 1)), (i+1)):
            #print ('j' + str(j))
            #print('spaceCount: ' + str(spaceCount))
            if((lowBound1<= pointsVisited[j][0] <= highBound1) & (lowBound2) <= pointsVisited[j][1] <= (highBound2)):
                spaceCount += 1
            else:
                spaceCount = 0
    #If there have been 4 consecutive moves in a row within the bounds, then click, and check if there should be a scroll
    if (spaceCount == cursorClick):
        print('Click')
        pyautogui.click()
        spaceCount = 0
        #If the cursor is near a scroll bar, then scroll, up or down
        scrollUpLoc = pyautogui.locateOnScreen('scrollUp.png')
        print('scrollUpLoc' + str(scrollUpLoc))
        scrollDownLoc = pyautogui.locateOnScreen('scrollDown.png')
        print('scrollDownLoc' + str(scrollDownLoc))
        x, y = pyautogui.position()
        if (scrollUpLoc != None):
            if (x > (scrollUpLoc[0] - 5) and x < (scrollUpLoc[0] + scrollUpLoc[2] + 5) and y > (scrollUpLoc[1] - 5) and y < (scrollUpLoc[1] + scrollUpLoc [3] + 5)):
                print ("Implement scroll up")
                pyautogui.scroll(5)
                print("Scrolled up")
        if (scrollDownLoc != None):
            if (x > (scrollDownLoc[0] - 5) and x < (scrollDownLoc[0] + scrollDownLoc[2] + 5) and y > (scrollDownLoc[1] - 5) and y < (scrollDownLoc[1] + scrollDownLoc [3] + 5)):
                print ("Implement scroll down")
                pyautogui.scroll(5)
                print("Scrolled down")
    i += 1






