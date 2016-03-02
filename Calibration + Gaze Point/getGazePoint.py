#Solutions obtained from 'Eye.MOV'
aOriginal = [576.217396, -24.047559, 1.0915599, -0.221105357, -0.025469321, 0.037511114]
bOriginal = [995.77047, -1.67122664, 12.67059, 0.018357141, 0.028264854, 0.012302]

def getGazePoint(solutionsA, solutionsB, pupilX, pupilY, glintX, glintY):
	"Returns the user's gaze point"
	
	#Calculate Delta X and Delta Y
	deltaX = pupilX - glintX
	deltaY = pupilY - glintY
	
	#Get X and Y coordinates 
	gazeX = solutionsA[0] + (solutionsA[1]*deltaX) + (solutionsA[2]*deltaY) + (solutionsA[3]*deltaX*deltaY) + (solutionsA[4]*(deltaX**2)) + (solutionsA[5]*(deltaY**2))
	
	gazeY = solutionsB[0] + (solutionsB[1]*deltaX) + (solutionsB[2]*deltaY) + (solutionsB[3]*deltaX*deltaY) + (solutionsB[4]*(deltaX**2)) + (solutionsB[5]*(deltaY**2))
	
	print gazeX
	print gazeY
	return (gazeX, gazeY);

getGazePoint(aOriginal, bOriginal, 648, 415, 626, 437)