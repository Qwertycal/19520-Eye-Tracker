import numpy as np

# 1366  x 768
# 153.6
# 76.8

def calibration(pupilX, pupilY, glintX, glintY, calibrationX, calibrationY):
    "Finds the unknown values in equation for relative gaze points"
	
	#X differences of glint-pupil vector
    deltaX = [(pupilX[0] - glintX[0]), (pupilX[1] - glintX[1]), (pupilX[2] - glintX[2]), (pupilX[3] - glintX[3]),
    (pupilX[4] - glintX[4]), (pupilX[5] - glintX[5]), (pupilX[6] - glintX[6]), (pupilX[7] - glintX[7]), (pupilX[8] - glintX[8])]

	#Y differences of glint-pupil vector
    deltaY = [(pupilY[0] - glintY[0]), (pupilY[1] - glintY[1]), (pupilY[2] - glintY[2]), (pupilY[3] - glintY[3]),
    (pupilY[4] - glintY[4]), (pupilY[5] - glintY[5]), (pupilY[6] - glintY[6]), (pupilY[7] - glintY[7]), (pupilY[8] - glintY[8])]
    

	#Equations matrix
    #2nd order (6 unknowns, 9 equations)
    a = np.array([[1, deltaX[0], deltaY[0], deltaX[0] * deltaY[0], deltaX[0]**2, deltaY[0]**2], 
                  [1, deltaX[1], deltaY[1], deltaX[1] * deltaY[1], deltaX[1]**2, deltaY[1]**2],
                  [1, deltaX[2], deltaY[2], deltaX[2] * deltaY[2], deltaX[2]**2, deltaY[2]**2],
                  [1, deltaX[3], deltaY[3], deltaX[3] * deltaY[3], deltaX[3]**2, deltaY[3]**2],
                  [1, deltaX[4], deltaY[4], deltaX[4] * deltaY[4], deltaX[4]**2, deltaY[4]**2],
                  [1, deltaX[5], deltaY[5], deltaX[5] * deltaY[5], deltaX[5]**2, deltaY[5]**2],
                  [1, deltaX[6], deltaY[6], deltaX[6] * deltaY[6], deltaX[6]**2, deltaY[6]**2],
                  [1, deltaX[7], deltaY[7], deltaX[7] * deltaY[7], deltaX[7]**2, deltaY[7]**2],
                  [1, deltaX[8], deltaY[8], deltaX[8] * deltaY[8], deltaX[8]**2, deltaY[8]**2]]) 
    print 'Equations matrix'
    print a

	#Answer matrix for x
	#2nd order (6 unknowns)
    b = np.array([[calibrationX[0]], [calibrationX[1]], [calibrationX[2]], [calibrationX[3]], [calibrationX[4]], [calibrationX[5]],
    [calibrationX[6]], [calibrationX[7]], [calibrationX[8]]])
    print 'Answer matrix for a'
    print b
    print 'Solutions for a'
    solutionA = np.linalg.lstsq(a,b)
    print solutionA[0]
	
	#Answer matrix for y
	#2nd order (6 unknowns)
    c = np.array([[calibrationY[0]], [calibrationY[1]], [calibrationY[2]], [calibrationY[3]], [calibrationY[4]], [calibrationY[5]],
    [calibrationY[6]], [calibrationY[7]], [calibrationY[8]]])		  
    print 'Answer matrix for b'
    print c
    print 'Solutions for b'
    solutionB = np.linalg.lstsq(a,c)
    print solutionB[0]
	
    return (solutionA[0], solutionB[0]);


            