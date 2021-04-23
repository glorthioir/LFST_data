#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 12:47:41 2018

@author: guillaume

Agent.py: class for the agent to analyse
"""

import random


class Agent():
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
        
        
    def move(self, nextPosition):
        self.position = nextPosition
        
    
    def heuristicComputation(self, pos1, pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


    def wallAvoidance(self, walls, height, width):
        stop = False
        direction = ''
        
        choices = ['up', 'right', 'down', 'left']
        while not stop:
            direction = choices[random.randint(0, len(choices)-1)]
            stop = True
            
            if direction == 'up':
                if self.position[1] == 0:
                    choices.remove('up')
                    stop = False
                    continue
                
                for wall in walls:
                    if wall[0][1] == wall[1][1] and wall[0][1] == self.position[1] and (self.position[0] <= wall[0][0] and self.position[0] >= wall[1][0] or self.position[0] >= wall[0][0] and self.position[0] <= wall[1][0]):
                        choices.remove('up')
                        stop = False
                        break
            
            elif direction == 'right':
                if self.position[0] == width-1:
                    choices.remove('right')
                    stop = False
                    continue
                
                for wall in walls:
                    if wall[0][0] == wall[1][0] and wall[0][0] == self.position[0]+1 and (self.position[1] <= wall[0][1] and self.position[1] >= wall[1][1] or self.position[1] >= wall[0][1] and self.position[1] <= wall[1][1]):
                        choices.remove('right')
                        stop = False
                        break
                
        
            elif direction == 'down':
                if self.position[1] == height-1:
                    choices.remove('down')
                    stop = False
                    continue
                
                for wall in walls:
                    if wall[0][1] == wall[1][1] and wall[0][1] == self.position[1]+1 and (self.position[0] <= wall[0][0] and self.position[0] >= wall[1][0] or self.position[0] >= wall[0][0] and self.position[0] <= wall[1][0]):
                        choices.remove('down')
                        stop = False
                        break

            elif direction == 'left':
                if self.position[0] == 0:
                    choices.remove('left')
                    stop = False
                    continue
                
                for wall in walls:
                    if wall[0][0] == wall[1][0] and wall[0][0] == self.position[1] and (self.position[1] <= wall[0][1] and self.position[1] >= wall[1][1] or self.position[1] >= wall[0][1] and self.position[1] <= wall[1][1]):
                        choices.remove('left')
                        stop = False
                        break
                        
        if direction == 'up':
            self.move((self.position[0], self.position[1]-1))
        elif direction == 'right':
            self.move((self.position[0]+1, self.position[1]))
        elif direction == 'down':
            self.move((self.position[0], self.position[1]+1))
        elif direction == 'left':
            self.move((self.position[0]-1, self.position[1]))
        else:
            return -1
                        
    
    def shortestWay(self, world, height, width, walls, end):
        openList = {self.position:(0, self.heuristicComputation(self.position, end))}
        closedList = {}
        currentNode = (self.position, openList[self.position][0], openList[self.position][1])
        path =[]
        cpt = 0
        
        while len(openList) > 0 and currentNode[0] != end:
            up, down, left, right = True, True, True, True 
            for wall in walls:
                
                if wall[0][1] == wall[1][1]:
                    if wall[0][1] == currentNode[0][1] and currentNode[0][0] >= min(wall[0][0], wall[1][0]) and currentNode[0][0] < max(wall[0][0], wall[1][0]):
                        up = False
                    elif wall[0][1] == currentNode[0][1]+1 and currentNode[0][0] >= min(wall[0][0], wall[1][0]) and currentNode[0][0] < max(wall[0][0], wall[1][0]):
                        down = False
                        
                if wall[0][0] == wall[1][0]:
                    if wall[0][0] == currentNode[0][0] and currentNode[0][1] >= min(wall[0][1], wall[1][1]) and currentNode[0][1] < max(wall[0][1], wall[1][1]):
                        left = False
                    elif wall[0][0] == currentNode[0][0]+1 and currentNode[0][1] >= min(wall[0][1], wall[1][1]) and currentNode[0][1] < max(wall[0][1], wall[1][1]):
                        right = False
                       
            if currentNode[0][0] > 0 and left:
                neighbour = ((currentNode[0][0]-1, currentNode[0][1]), currentNode[1]+1, self.heuristicComputation((currentNode[0][0]-1, currentNode[0][1]), end)) 
                if neighbour[0] not in closedList:
                    if neighbour[0] not in openList:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                    elif openList[neighbour[0]][0]+openList[neighbour[0]][1] > neighbour[1]+neighbour[2]:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                
            if currentNode[0][0] < width-1 and right:
                neighbour = ((currentNode[0][0]+1, currentNode[0][1]), currentNode[1]+1, self.heuristicComputation((currentNode[0][0]+1, currentNode[0][1]), end)) 
                if neighbour[0] not in closedList:
                    if neighbour[0] not in openList:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                    elif openList[neighbour[0]][0]+openList[neighbour[0]][1] > neighbour[1]+neighbour[2]:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                
            if currentNode[0][1] > 0 and up:
                neighbour = ((currentNode[0][0], currentNode[0][1]-1), currentNode[1]+1, self.heuristicComputation((currentNode[0][0], currentNode[0][1]-1), end)) 
                if neighbour[0] not in closedList:
                    if neighbour[0] not in openList:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                    elif openList[neighbour[0]][0]+openList[neighbour[0]][1] > neighbour[1]+neighbour[2]:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                
            if currentNode[0][1] < height-1 and down:
                neighbour = ((currentNode[0][0], currentNode[0][1]+1), currentNode[1]+1, self.heuristicComputation((currentNode[0][0], currentNode[0][1]+1), end)) 
                if neighbour[0] not in closedList:
                    if neighbour[0] not in openList:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])
                    elif openList[neighbour[0]][0]+openList[neighbour[0]][1] > neighbour[1]+neighbour[2]:
                        openList[neighbour[0]] = (neighbour[1], neighbour[2])

            openList.pop(currentNode[0])
            nodeMin = (currentNode[0], currentNode[1]+width, currentNode[2]+height) 
            for node in openList:
                
                if openList[node][0]+openList[node][1] < nodeMin[1]+nodeMin[2]:
                    nodeMin = (node, openList[node][0], openList[node][1])
                elif openList[node][0]+openList[node][1] == nodeMin[1]+nodeMin[2] and openList[node][1] < nodeMin[2]:
                    nodeMin = (node, openList[node][0], openList[node][1])
                    
            path.append((currentNode[0], nodeMin[0]))
            closedList[currentNode[0]]=(currentNode[1], currentNode[2])
            currentNode = nodeMin

            cpt += 1
            if cpt > 10000:
                return None
            
        tmpPath = []
        currentNode = end        
        for i in range(1, len(path)+1):
            if path[-i][1] == currentNode:
                tmpPath.append(currentNode)
                currentNode = path[-i][0]
        
        tmpPath.append(currentNode)
        
        shortestPath = [tmpPath.pop(0)]
        pathSize = len(tmpPath)
        for i in range(pathSize):
            elem = tmpPath.pop(0)
            if self.heuristicComputation(elem, shortestPath[-1]) == 1:
                shortestPath.append(elem)
        
        shortestPath.reverse()
        shortestPath.append(end)
        
        return shortestPath
            

    def ballGame(self, worldSize, nbPot):
        world = [{"pot" : 0} for i in range(worldSize)]  
        evenNumbers = [n for n in range(worldSize) if n%2 == 0]    
        trace = []
        
        for number in range(worldSize):
            if number%2 == 0:
                world[number]["cell"] = "white"
            else:
                world[number]["cell"] = "black"
        
        winningPos = evenNumbers[random.randint(0, len(evenNumbers)-1)]
        world[winningPos]["pot"] = 1
        nbPot -= 1
        
        listOfPos = [number for number in range(worldSize) if number != winningPos]
        i = 2
        while nbPot > 0:
            potPos = listOfPos[random.randint(0, worldSize-i)]
            world[potPos]["pot"] = 1
            listOfPos.remove(potPos)
            nbPot -= 1
            i += 1
            
        goal = 0
        potOnLeft = 0
        potOnRight = 0
        pos = 0
        pot = 0
        cellColor = "white"
        cpt = 0
        
        while goal == 0:
            
            if cpt > 9 :
                pos = winningPos
            else:
                pos = random.randint(0, worldSize-1)
                cpt += 1
                        
            if pos > 0:
                potOnLeft = world[pos-1]["pot"]
            else:
                potOnLeft = 0
                
            if pos < worldSize-1:
                potOnRight = world[pos+1]["pot"]
            else:
                potOnRight = 0
            
            if world[pos]["cell"] == "white" and world[pos]["pot"] == 1:
                goal = 1
            else:
                goal = 0
                
            pot = world[pos]["pot"]
            cellColor = world[pos]["cell"]
            
            trace.append({"pos" : pos, "cellColor" : cellColor, "pot" : pot, "potOnLeft" : potOnLeft, "potOnRight" : potOnRight, "goal" : goal})
            
        return trace, world

    
    def cubeWorld(self, worldSize):
        world = [ [] for i in range(worldSize)]
        cubes = ["cube1", "cube2", "cube3", "cube4", "cube5", "cube6"]
        trace = []
        ready = False
        
        while not ready:
            ready = True
            listCube = list(cubes)
            
            while len(listCube) > 0:
                cube = listCube.pop(random.randint(0, len(listCube)-1))
                world[random.randint(0, worldSize-1)].append(cube)
                
            for pile in world:
                if len(pile) < 3:
                    continue
                #elif (pile[0] == "cube2" and pile[1] == "cube1" and pile[2] == "cube3") or (pile[0] == "cube3" and pile[1] == "cube1" and pile[2] == "cube2"):
                elif (pile[0] == "cube2" and pile[1] == "cube1" and pile[2] == "cube3"):   
                    ready = False
                    break
        
        goal = 0  
        cubePos = {"cube"+str(i):0 for i in range(1,6)}
        cubeH = {"cube"+str(i):0 for i in range(1,6)}
        
        for i in range(len(world)):
            for j in range(len(world[i])):
                cubePos[world[i][j]] = i
                cubeH[world[i][j]] = j
                
#        goalType = random.randint(0, 1)
        goalType = 0
        piles = [i for i in range(worldSize)]
        piles2 = [i for i in range(worldSize)]
        piles3 = [i for i in range(worldSize)]
        pilesBis = [i for i in range(worldSize)]
        piles2Bis = [i for i in range(worldSize)]
        piles3Bis = [i for i in range(worldSize)]
        pileCible = None
        pileCible2 = None
        
        while goal == 0:
            
            newPos = {key+"Pos":cubePos[key] for key in cubePos.keys()}
            newH = {key+"H":cubeH[key] for key in cubeH.keys()}
            dico = {**newPos, **newH, 'goal':goal}
            trace.append(dict(dico)) 
            
            if goalType == 0: # cube2 / cube1 / cube3
                
                if cubeH["cube2"] != 0:
                    
                    if cubePos["cube2"] in piles:
                        piles.remove(cubePos["cube2"])
                        
                    if len(world[cubePos["cube2"]])-1 > cubeH["cube2"]:         # On enleve les cubes au dessus
                        cube = world[cubePos["cube2"]].pop(-1)
                        newPile = piles[random.randint(0, len(piles)-1)]
                        world[newPile].append(cube)
                        cubePos[cube] = newPile
                        cubeH[cube] = len(world[newPile])-1
                        
                    else:
                        
                        if pileCible == None:
                            pileCible = piles[random.randint(0, len(piles)-1)]      # On choisi une pile cible
                            piles.remove(pileCible)
                        
                        if len(world[pileCible]) > 0:                           # On nettoie la pile cible
                            cube = world[pileCible].pop(-1)
                            newPile = piles[random.randint(0, len(piles)-1)]
                            world[newPile].append(cube)
                            cubePos[cube] = newPile
                            cubeH[cube] = len(world[newPile])-1
                            
                        else:
                            cube = world[cubePos["cube2"]].pop(-1)
                            world[pileCible].append(cube)
                            cubePos[cube] = pileCible
                            cubeH[cube] = len(world[pileCible])-1
                        
                elif cubeH["cube1"] != 1 or cubePos["cube1"] != cubePos["cube2"]:
                    
                    if cubePos["cube1"] in piles2:
                        piles2.remove(cubePos["cube1"])
                    if cubePos["cube2"] in piles2:
                        piles2.remove(cubePos["cube2"])
                    
                    if cubePos["cube1"] != cubePos["cube2"]:        # Checker pour le mettre sur la pile du 2
                        
                        if len(world[cubePos["cube2"]]) > 1:
                             cube = world[cubePos["cube2"]].pop(-1)
                             newPile = piles2[random.randint(0, len(piles2)-1)]
                             world[newPile].append(cube)
                             cubePos[cube] = newPile
                             cubeH[cube] = len(world[newPile])-1
                             
                        else:
                            
                            if len(world[cubePos["cube1"]])-1 > cubeH["cube1"]:
                                cube = world[cubePos["cube1"]].pop(-1)
                                newPile = piles2[random.randint(0, len(piles2)-1)]
                                world[newPile].append(cube)
                                cubePos[cube] = newPile
                                cubeH[cube] = len(world[newPile])-1
                                
                            else:
                                cube = world[cubePos["cube1"]].pop(-1)
                                world[cubePos["cube2"]].append(cube)
                                cubePos[cube] = cubePos["cube2"]
                                cubeH[cube] = len(world[cubePos["cube2"]])-1
                                
                    else:
                        
                        cube = world[cubePos["cube1"]].pop(-1)
                        newPile = piles2[random.randint(0, len(piles2)-1)]
                        world[newPile].append(cube)
                        cubePos[cube] = newPile
                        cubeH[cube] = len(world[newPile])-1
                                
                else:
                    
                    if cubePos["cube1"] in piles3:
                        piles3.remove(cubePos["cube1"])
                    if cubePos["cube3"] in piles3:
                        piles3.remove(cubePos["cube3"])
                    
                    if cubePos["cube1"] != cubePos["cube3"]:        # Checker pour le mettre sur la pile du 2
                        
                        if len(world[cubePos["cube1"]]) > 2:
                             cube = world[cubePos["cube1"]].pop(-1)
                             newPile = piles3[random.randint(0, len(piles3)-1)]
                             world[newPile].append(cube)
                             cubePos[cube] = newPile
                             cubeH[cube] = len(world[newPile])-1
                             
                        else:
                            
                            if len(world[cubePos["cube3"]])-1 > cubeH["cube3"]:
                                cube = world[cubePos["cube3"]].pop(-1)
                                newPile = piles3[random.randint(0, len(piles3)-1)]
                                world[newPile].append(cube)
                                cubePos[cube] = newPile
                                cubeH[cube] = len(world[newPile])-1
                                
                            else:
                                cube = world[cubePos["cube3"]].pop(-1)
                                world[cubePos["cube1"]].append(cube)
                                cubePos[cube] = cubePos["cube1"]
                                cubeH[cube] = len(world[cubePos["cube1"]])-1
                                
                    else:

                        cube = world[cubePos["cube3"]].pop(-1)
                        newPile = piles3[random.randint(0, len(piles3)-1)]
                        world[newPile].append(cube)
                        cubePos[cube] = newPile
                        cubeH[cube] = len(world[newPile])-1

                        
            for pile in world:
                if len(pile) < 3:
                    continue
                elif pile[0] == "cube2" and pile[1] == "cube1" and pile[2] == "cube3":
                    goal = 1
                    break
        
        newPos = {key+"Pos":cubePos[key] for key in cubePos.keys()}
        newH = {key+"H":cubeH[key] for key in cubeH.keys()}                
        dico = {**newPos, **newH, 'goal':goal}
        trace.append(dict(dico))
                
        return trace, world




    def playTo421(self, numberOfDices):
        trace = []
        dices = {"dice"+str(n):1 for n in range(1,numberOfDices+1)}
        dicesToChange = [k for k in dices.keys()]
        elemToHave = [4, 2, 1]
        goal = 0

        dTmp = dict(dices)
        dTmp["goal"] = goal
        trace.append(dTmp)

        while goal == 0:

            dicesToChangeTmp = list(dicesToChange)

            for elem in dicesToChangeTmp:
                dices[elem] = random.randint(1,6)
                if dices[elem] in elemToHave:
                    elemToHave.remove(dices[elem])
                    dicesToChange.remove(elem)

            if elemToHave == []:
                goal = 1

            dTmp = dict(dices)
            dTmp["goal"] = goal
            trace.append(dTmp)

        return trace


























    
            
        
        
        
