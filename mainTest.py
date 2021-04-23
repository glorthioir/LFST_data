import random

from Agent import *
from generator import *
from prologConvertor import *
from learning import *
from gridWalls16_16 import *


###========== Initial parameters ==========###

height = 16
width = 16
zoom = 40
 
agentPosition = (15, 12)
endPosition = (0, 0)
nbrStartPos = 16
pWall = 0.6
pColor = [1, 0, 0]    # white, green and red
colorTable = {'white':"#FFFFFF", 'green':"green", 'red':"red", 'grey':"#E8E8EB", 'agent':"#F9FB70"}
outputFiles = {"gridWorld":"grid_data.txt", "cubeWorld":"cube_data.txt", "421World":"421_data.txt"} 

cubeWorldsize = 3
nbGamesCube = 100

nbGames421 = 100
nbDices = 4
winningNumbers = [4, 2, 1]+[0 for n in range(0,nbDices-3) ] 




###========== Setting up the environment ==========###

listOfWalls = [walls_16_16_1, walls_16_16_2, walls_16_16_4, walls_16_16_5, walls_16_16_7, walls_16_16_8, walls_16_16_10, walls_16_16_11]
listOfEndPosition = [goal_16_16_1, goal_16_16_2, goal_16_16_4, goal_16_16_5, goal_16_16_7, goal_16_16_8, goal_16_16_10, goal_16_16_11]

#walls, endPosition = wallsGenerator(height, width, pWall, "down")			# Use this one if you want to generate a random grid and goal position for GridWorld
world = worldGenerator(width, height, 0, pColor, agentPosition, endPosition)




###========== Setting up the agent ==========### 

agent = Agent("Bond", agentPosition)

listOfPaths = []		# traces for GridWorld

for i in range(len(listOfWalls)):
	paths = []
	startPositions = []
	startPositionsTmp = [elem for elem in listOfEndPosition if elem != listOfEndPosition[i]]

	for elem in startPositionsTmp:
		agent.move(elem)
		path = agent.shortestWay(world, height, width, listOfWalls[i], listOfEndPosition[i])
		if path != None:
			startPositions.append(elem)
			paths.append(path)
				
	while len(startPositions) < nbrStartPos:
		p = (random.randint(0, height-1), random.randint(0, width-1))
		agent.move(p)
		path = agent.shortestWay(world, height, width, listOfWalls[i], listOfEndPosition[i])
		while p in startPositions or path == None:
			p = (random.randint(0, height-1), random.randint(0, width-1))
			agent.move(p)
			path = agent.shortestWay(world, height, width, listOfWalls[i], listOfEndPosition[i])
		
		startPositions.append(p)
		paths.append(path)

	listOfPaths.append(paths)
	
listOfActions = []
for i in range(len(listOfWalls)):
	possibilities, actions = behaviorsAnalyse(world, listOfWalls[i], height, width, listOfPaths[i])
	listOfActions.append(actions)

listOfTransitions = []
for k in range(len(listOfWalls)):  
	transitions = []
	actions = listOfActions[k]
	paths = listOfPaths[k]
	for i in range(len(actions)):
		transition = []
		for j in range(len(actions[i])):
			transition.append((paths[i][j], actions[i][j]))  
		transitions.append(transition)
	listOfTransitions.append(transitions)


listOfTracesCube = []		# traces for CubeWorld

for n in range(nbGamesCube):
    traces, world = agent.cubeWorld(cubeWorldsize)
    listOfTracesCube.append(traces)


listOfTraces421 = []		# traces for 421World

for n in range(nbGames421):
    traces421 = agent.playTo421(nbDices)
    listOfTraces421.append(traces421)



###========== Collect the data ==========### 

listOfVariables = []
for i in range(len(listOfWalls)):
	variables = dataWriter(outputFiles["gridWorld"], listOfWalls[i], listOfTransitions[i], width, height, listOfEndPosition[i])
	listOfVariables += variables

listOfVariables = traceCleaning(["closer", "move"], listOfVariables) 
positives, negatives = convertorTracesExamples(listOfVariables)				# convert the trace into the positive and negative set of examples

positivesCube, negativesCube = convertorTracesExamples(listOfTracesCube)

positives421, negatives421 = convertorTracesExamples(listOfTraces421)
 

csvFileWriter(positives, negatives, outputFiles["gridWorld"])
csvFileWriter(positivesCube, negativesCube, outputFiles["cubeWorld"]) 
csvFileWriter(positives421, negatives421, outputFiles["421World"])

print("The data have been successfully generated in the following files :")
for file in outputFiles:
	print("----->", outputFiles[file])
   














