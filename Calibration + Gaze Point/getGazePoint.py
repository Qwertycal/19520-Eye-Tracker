def getGazePoint(solutionsA, solutionsB, pupilX, pupilY, glintX, glintY):
	"Returns the user's gaze point"
	
	#Calculate Delta X and Delta Y
	deltaX = pupilX - glintX
	deltaY = pupilY - glintY
	
	#Get X and Y coordinates 
	gazeX = solutionsA[0] + (solutionsA[1]*deltaX) + (solutionsA[2]*deltaY) + (solutionsA[3]*deltaX*deltaY) + (solutionsA[4]*(deltaX**2)) + (solutionsA[5]*(deltaY**2))
	
	gazeY = solutionsB[0] + (solutionsB[1]*deltaX) + (solutionsB[2]*deltaY) + (solutionsB[3]*deltaX*deltaY) + (solutionsB[4]*(deltaX**2)) + (solutionsB[5]*(deltaY**2))
    
	return (gazeX, gazeY)
