import pyautogui
spaceCount = 0

coords = [(100, 100), (110, 90),(90, 110), (103, 104), (98, 97), (102, 104)]
maxMovement = 10

for i in range (0, len(coords)):
    pyautogui.moveTo(coords[i], duration=0.25)

    if (i>3):
        #print('i: ' + str(i) + '; i-4: ' + str(i-4))
        lowBound1 = (coords[i-4][0])-maxMovement
        lowBound2 = (coords[i-4][1])-maxMovement
        highBound1 = (coords[i-4][0])+maxMovement
        highBound2 = (coords[i-4][1])+maxMovement
        spaceCount = 0

        for j in range((i-3), (i+1)):
            print('j: ' + str(j))
            # print('Coords 0: ' + str(coords[j][0]) + ' Coords 1: ' + str(coords[j][1]))
            # print('LB1 ' + str(lowBound1) + ', HB1 ' + str(highBound1) + '\n' +
            # ' LB2 ' + str(lowBound2) + ' HB2 ' + str(highBound2))
            if((lowBound1<= coords[j][0] <= highBound1) & (lowBound2) <= coords[j][1] <= (highBound2)):
                spaceCount += 1
            #print('spaceCount: ' + str(spaceCount))
            else:
                spaceCount = 0
    if (spaceCount == 4):
        print('Click')
        pyautogui.click()