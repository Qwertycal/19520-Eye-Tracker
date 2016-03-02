import numpy as np

# 1366  x 768
# 153.6
# 76.8

def calibration(pupilX1, pupilY1, glintX1, glintY1, pupilX2, pupilY2, glintX2, glintY2,
pupilX3, pupilY3, glintX3, glintY3, pupilX4, pupilY4, glintX4, glintY4, pupilX5, pupilY5, 
glintX5, glintY5, pupilX6, pupilY6, glintX6, glintY6, pupilX7, pupilY7, glintX7, glintY7,
pupilX8, pupilY8, glintX8, glintY8, pupilX9, pupilY9, glintX9, glintY9, pupilX10, pupilY10,
glintX10, glintY10, pupilX11, pupilY11, glintX11, glintY11):
	"Finds the unknown values in equation for relative gaze points"
	
	#X coordinates of the points of calibration
	calibrationX1 = 136
	calibrationX2 = 1228
	calibrationX3 = 683
	calibrationX4 = 403
	calibrationX5 = 937
	calibrationX6 = 683
	calibrationX7 = 683
	calibrationX8 = 937
	calibrationX9 = 403
	calibrationX10 = 403
	calibrationX11 = 937

	#Y coordinates of the points of calibration
	calibrationY1 = 691
	calibrationY2 = 691
	calibrationY3 = 384
	calibrationY4 = 384
	calibrationY5 = 384
	calibrationY6 = 230
	calibrationY7 = 547
	calibrationY8 = 230
	calibrationY9 = 230
	calibrationY10 = 547
	calibrationY11 = 547

	#Example x differences of glint-pupil vector
	deltaX1 = pupilX1 - glintX1
	deltaX2 = pupilX2 - glintX2
	deltaX3 = pupilX3 - glintX3
	deltaX4 = pupilX4 - glintX4
	deltaX5 = pupilX5 - glintX5
	deltaX6 = pupilX6 - glintX6
	deltaX7 = pupilX7 - glintX7
	deltaX8 = pupilX8 - glintX8
	deltaX9 = pupilX9 - glintX9
	deltaX10 = pupilX10 - glintX10
	deltaX11 = pupilX11 - glintX11

	#Example y differences of glint-pupil vector
	deltaY1 = pupilY1 - glintY1
	deltaY2 = pupilY2 - glintY2
	deltaY3 = pupilY3 - glintY3
	deltaY4 = pupilY4 - glintY4
	deltaY5 = pupilY5 - glintY5
	deltaY6 = pupilY6 - glintY6
	deltaY7 = pupilY7 - glintY7
	deltaY8 = pupilY8 - glintY8
	deltaY9 = pupilY9 - glintY9
	deltaY10 = pupilY10 - glintY10
	deltaY11 = pupilY11 - glintY11
		
	#Equations matrix
	#2nd order - Calib3rdOrderPaper
	a2 = np.array([[1, pupilX1, pupilY1, pupilX1**2, pupilX1*pupilY1, pupilY1**2],
				   [1, pupilX2, pupilY2, pupilX2**2, pupilX2*pupilY2, pupilY2**2],
				   [1, pupilX3, pupilY3, pupilX3**2, pupilX3*pupilY3, pupilY3**2],
				   [1, pupilX4, pupilY4, pupilX4**2, pupilX4*pupilY4, pupilY4**2],
				   [1, pupilX5, pupilY5, pupilX5**2, pupilX5*pupilY5, pupilY5**2],
				   [1, pupilX6, pupilY6, pupilX6**2, pupilX6*pupilY6, pupilY6**2]])
	
	
	#3rd order - Calib3rdOrderPaper
	# entry 7 has 2 coefficients 
	a3 = np.array([[1, pupilX1, pupilY1, pupilX1**2, pupilX1*pupilY1, pupilY1**2, (pupilX1**3) * pupilY1, pupilX1 * (pupilY1**2), pupilY1**3],
				   [1, pupilX2, pupilY2, pupilX2**2, pupilX2*pupilY2, pupilY2**2, (pupilX2**3) * pupilY2, pupilX2 * (pupilY2**2), pupilY2**3],
				   [1, pupilX3, pupilY3, pupilX3**2, pupilX3*pupilY3, pupilY3**2, (pupilX3**3) * pupilY3, pupilX3 * (pupilY3**2), pupilY3**3],
				   [1, pupilX4, pupilY4, pupilX4**2, pupilX4*pupilY4, pupilY4**2, (pupilX4**3) * pupilY4, pupilX4 * (pupilY4**2), pupilY4**3],
				   [1, pupilX5, pupilY5, pupilX5**2, pupilX5*pupilY5, pupilY5**2, (pupilX5**3) * pupilY5, pupilX5 * (pupilY5**2), pupilY5**3],
				   [1, pupilX6, pupilY6, pupilX6**2, pupilX6*pupilY6, pupilY6**2, (pupilX6**3) * pupilY6, pupilX6 * (pupilY6**2), pupilY6**3],
				   [1, pupilX7, pupilY7, pupilX7**2, pupilX7*pupilY7, pupilY7**2, (pupilX7**3) * pupilY7, pupilX7 * (pupilY7**2), pupilY7**3],
				   [1, pupilX8, pupilY8, pupilX8**2, pupilX8*pupilY8, pupilY8**2, (pupilX8**3) * pupilY8, pupilX8 * (pupilY8**2), pupilY8**3],
				   [1, pupilX9, pupilY9, pupilX9**2, pupilX9*pupilY9, pupilY9**2, (pupilX9**3) * pupilY9, pupilX9 * (pupilY9**2), pupilY9**3],
				   [1, pupilX10, pupilY10, pupilX10**2, pupilX10*pupilY10, pupilY10**2, (pupilX10**3) * pupilY10, pupilX10 * (pupilY10**2), pupilY10**3]])

	#Original - Paper 7 "A Low-cost Head Supported Eye Tracker with High Precision
	a = np.array([[1, deltaX1, deltaY1, deltaX1 * deltaY1, deltaX1**2, deltaY1**2], 
				  [1, deltaX2, deltaY2, deltaX2 * deltaY2, deltaX2**2, deltaY2**2],
				  [1, deltaX3, deltaY3, deltaX3 * deltaY3, deltaX3**2, deltaY3**2],
				  [1, deltaX4, deltaY4, deltaX4 * deltaY4, deltaX4**2, deltaY4**2],
				  [1, deltaX5, deltaY5, deltaX5 * deltaY5, deltaX5**2, deltaY5**2],
				  [1, deltaX6, deltaY6, deltaX6 * deltaY6, deltaX6**2, deltaY6**2]]) 
	print 'Equations matrix'
	print a

	#Answer matrix for x
	#3rd order - Calib3rdOrderPaper
	b3 = np.array([[calibrationX1], [calibrationX2], [calibrationX3], [calibrationX4], [calibrationX5], [calibrationX6], [calibrationX7], 
				   [calibrationX8], [calibrationX9], [calibrationX10]])
	
	#Original - Paper 7 "A Low-cost Head Supported Eye Tracker with High Precision / 2nd order - Calib3rdOrderPaper
	b = np.array([[calibrationX1], [calibrationX2], [calibrationX3], [calibrationX4],
				  [calibrationX5], [calibrationX6]])
				  
	print 'Answer matrix for a'
	print b
	print 'Solutions for a'
	solutionA = np.linalg.solve(a,b)
	print solutionA
	
	#Answer matrix for y
	#3rd order - Calib3rdOrderPaper
	c3 = np.array([[calibrationY1], [calibrationY2], [calibrationY3], [calibrationY4], [calibrationY5], [calibrationY6], [calibrationY7], 
				   [calibrationY8], [calibrationY9], [calibrationY10]])
	
	#Original - Paper 7 "A Low-cost Head Supported Eye Tracker with High Precision / 2nd order - Calib3rdOrderPaper
	c = np.array([[calibrationY1], [calibrationY2], [calibrationY3], [calibrationY4],
				  [calibrationY5], [calibrationY6]])
				  
	print 'Answer matrix for b'
	print c
	print 'Solutions for b'
	solutionB = np.linalg.solve(a,c)
	print solutionB
	
	return (solutionA, solutionB);

calibration(648, 415, 626, 437, 516, 379, 560, 417, 591, 355, 596, 407, 630, 367, 615, 415, 542, 344, 571, 404, 593, 334, 595, 399, 585, 382, 594, 420, 546, 320, 571, 395, 634, 341, 614, 405, 629, 388, 615, 424, 537, 367, 571, 412)