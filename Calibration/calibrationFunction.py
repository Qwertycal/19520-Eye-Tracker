import numpy as np

def calibration(pupilX1, pupilY1, glintX1, glintY1, pupilX2, pupilY2, glintX2, glintY2,
pupilX3, pupilY3, glintX3, glintY3, pupilX4, pupilY4, glintX4, glintY4, pupilX5, pupilY5, 
glintX5, glintY5, pupilX6, pupilY6, glintX6, glintY6):
	"Finds the unknown values in equation for relative gaze points"
	
	#X coordinates of the points of calibration
	calibrationX1 = 2
	calibrationX2 = 4
	calibrationX3 = 6
	calibrationX4 = 8
	calibrationX5 = 10
	calibrationX6 = 12

	#Y coordinates of the points of calibration
	calibrationY1 = 3
	calibrationY2 = 6
	calibrationY3 = 9
	calibrationY4 = 12
	calibrationY5 = 15
	calibrationY6 = 18

	#Example x differences of glint-pupil vector
	deltaX1 = pupilX1 - glintX1
	deltaX2 = pupilX2 - glintX2
	deltaX3 = pupilX3 - glintX3
	deltaX4 = pupilX4 - glintX4
	deltaX5 = pupilX5 - glintX5
	deltaX6 = pupilX6 - glintX6

	#Example y differences of glint-pupil vector
	deltaY1 = pupilY1 - glintY1
	deltaY2 = pupilY2 - glintY2
	deltaY3 = pupilY3 - glintY3
	deltaY4 = pupilY4 - glintY4
	deltaY5 = pupilY5 - glintY5
	deltaY6 = pupilY6 - glintY6

	#Equations matrix
	a = np.array([[1, deltaX1, deltaY1, deltaX1 * deltaY1, deltaX1**2, deltaY1**2], 
	[1, deltaX2, deltaY2, deltaX2 * deltaY2, deltaX2**2, deltaY2**2],
	[1, deltaX3, deltaY3, deltaX3 * deltaY3, deltaX3**2, deltaY3**2],
	[1, deltaX4, deltaY4, deltaX4 * deltaY4, deltaX4**2, deltaY4**2],
	[1, deltaX5, deltaY5, deltaX5 * deltaY5, deltaX5**2, deltaY5**2],
	[1, deltaX6, deltaY6, deltaX6 * deltaY6, deltaX6**2, deltaY6**2]]) 
	print 'Equations matrix'
	print a

	#Answer matrix for x
	b = np.array([[calibrationX1], [calibrationX2], [calibrationX3], [calibrationX4],
	[calibrationX5], [calibrationX6]])
	print 'Answer matrix for a'
	print b
	print 'Solutions for a'
	solutionA = np.linalg.solve(a,b)
	print solutionA
	
	#Answer matrix for y
	c = np.array([[calibrationY1], [calibrationY2], [calibrationY3], [calibrationY4],
	[calibrationY5], [calibrationY6]])
	print 'Answer matrix for b'
	print c
	print 'Solutions for b'
	solutionB = np.linalg.solve(a,c)
	print solutionB
	return (solutionA, solutionB);

calibration(4, 7, 3, 8, 1, 6, 6, 9, 2, 5, 6, 7, 4, 3, 6, 8, 2, 4, 6, 1, 5, 7, 9, 3)