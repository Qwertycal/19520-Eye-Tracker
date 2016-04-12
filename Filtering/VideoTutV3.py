import sys
import cv2

i = 0
found = False


for i in range(4):
	capture = cv2.VideoCapture(i)
    if not capture:
        print "UNABLE TO CAPTURE CAMERA"
    else:
        found = True
        print "taken camera from index: ", i
        break

if found == False:
    print "!!! No camera was found."
    sys.exit()