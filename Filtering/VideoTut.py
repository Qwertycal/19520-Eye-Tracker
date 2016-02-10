import numpy as np
import cv2

# create an object for the video, the argument is the number of the 
# camera, in this case only one. Replace with path or file 
# name to play from file
cap = cv2.VideoCapture(1)
win_length = cap.get(3)
win_height = cap.get(4) 
print 'length', win_length
print 'height', win_height

while(True):
	#Capture frame by frame from object
	# returns a boolean TRUE if frame is read correctly
	ret, frame = cap.read()

	#Operations on a frame - convert to greyscale
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Original RGB feed from webcam
	cv2.imshow('original', frame)

	# Show the resulting frame
	#cv2.imshow('frame',gray)

	#close everything when q is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()