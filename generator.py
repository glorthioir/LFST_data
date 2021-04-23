#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:11:42 2018

@author: guillaume

generator.py contains the functions needed to generate the world
"""

import random


class Case:
    def __init__(self, wall, color):
        self.wall = wall
        self.color = color
        
        
def worldGenerator(width, height, pWall, pColor, agentPosition, endPos):
    world = []

    for i in range(height):
        for j in range(width):
            wall = random.random() < pWall

            if (j, i) == endPos:
                world.append(Case(wall, "green"))
            
            elif wall and (j,i) != agentPosition:
                world.append(Case(wall, "grey"))
                
            else:
                choice = random.random()
                if choice < pColor[0]:
                    world.append(Case(wall, "white"))
                elif choice < pColor[0] + pColor[1]:
                    world.append(Case(wall, "green"))
                else:
                    world.append(Case(wall, "red"))
                    
    return world


def cubeWorldGenerator(nbCubes):
    listOfCubes = []
    listOfColumns = [0 for i in range(nbCubes)]
    
    for i in range(nbCubes):
        
        x = random.randint(0, nbCubes-1)
        y = listOfColumns[x]
        listOfColumns[x] += 1
        listOfCubes.append((x, y))
        
    return listOfCubes


def wallsGenerator(height, width, pWall, doorOrientation = None):
    goal = None
    listOfWalls = []
    cellsWallingDict = {(i, j):[] for i in range(height) for j in range(width)} # (i, j):["up", "right", "down", "left"]
    
    if doorOrientation == None:
        goal = (random.randint(0, height-1), random.randint(0, width-1))

        doorPos = ["up", "right", "down", "left"]

        if goal[0] == 0:
            doorPos.remove("up")
        if goal[0] == height-1:
            doorPos.remove("down")
        if goal[1] == 0:
            doorPos.remove("left")
        if goal[1] == width-1:
            doorPos.remove("right")

        doorPos = random.choice(doorPos)

    else:
        doorPos = doorOrientation
        if doorPos == "up":
            goal = (random.randint(1, height-1), random.randint(0, width-1))
        elif doorPos == "right":
            goal = (random.randint(0, height-1), random.randint(0, width-2))
        elif doorPos == "down":
            goal = (random.randint(0, height-2), random.randint(0, width-1))
        else:
            goal = (random.randint(0, height-1), random.randint(1, width-1))

    if doorPos == "up":

        cellsWallingDict[goal] = ["right", "down", "left"]
        neighborR = (goal[0], goal[1]+1)
        neighborD = (goal[0]+1, goal[1])
        neighborL = (goal[0], goal[1]-1)

        if neighborR in cellsWallingDict:
            cellsWallingDict[neighborR].append("left")
        if neighborD in cellsWallingDict:
            cellsWallingDict[neighborD].append("up")
        if neighborL in cellsWallingDict:
            cellsWallingDict[neighborL].append("right")

        listOfWalls.append(((goal[0], goal[1]), (goal[0]+1, goal[1])))
        listOfWalls.append(((goal[0]+1, goal[1]), (goal[0]+1, goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]+1), (goal[0]+1, goal[1]+1)))

    if doorPos == "right":

        cellsWallingDict[goal] = ["up", "down", "left"]
        neighborU = (goal[0]-1, goal[1])
        neighborD = (goal[0]+1, goal[1])
        neighborL = (goal[0], goal[1]-1)

        if neighborU in cellsWallingDict:
            cellsWallingDict[neighborU].append("down")
        if neighborD in cellsWallingDict:
            cellsWallingDict[neighborD].append("up")
        if neighborL in cellsWallingDict:
            cellsWallingDict[neighborL].append("right")

        listOfWalls.append(((goal[0], goal[1]), (goal[0], goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]), (goal[0]+1, goal[1])))
        listOfWalls.append(((goal[0]+1, goal[1]), (goal[0]+1, goal[1]+1)))

    if doorPos == "down":

        cellsWallingDict[goal] = ["up", "right", "left"]
        neighborR = (goal[0], goal[1]+1)
        neighborU = (goal[0]-1, goal[1])
        neighborL = (goal[0], goal[1]-1)

        if neighborR in cellsWallingDict:
            cellsWallingDict[neighborR].append("left")
        if neighborU in cellsWallingDict:
            cellsWallingDict[neighborU].append("down")
        if neighborL in cellsWallingDict:
            cellsWallingDict[neighborL].append("right")

        listOfWalls.append(((goal[0], goal[1]+1), (goal[0]+1, goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]), (goal[0], goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]), (goal[0]+1, goal[1])))

    if doorPos == "left":

        cellsWallingDict[goal] = ["up", "right", "down"]
        neighborR = (goal[0], goal[1]+1)
        neighborD = (goal[0]+1, goal[1])
        neighborU = (goal[0]-1, goal[1])

        if neighborR in cellsWallingDict:
            cellsWallingDict[neighborR].append("left")
        if neighborD in cellsWallingDict:
            cellsWallingDict[neighborD].append("up")
        if neighborU in cellsWallingDict:
            cellsWallingDict[neighborU].append("down")

        listOfWalls.append(((goal[0]+1, goal[1]), (goal[0]+1, goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]+1), (goal[0]+1, goal[1]+1)))
        listOfWalls.append(((goal[0], goal[1]), (goal[0], goal[1]+1)))

    for i in range(height):
        for j in range(width):
            wall = random.random() < pWall

            if wall:

                newWall = None
                neighborU = (i-1, j)
                neighborL = (i, j-1)

                if random.random() < 0.5:
                    if neighborU not in cellsWallingDict or len(cellsWallingDict[neighborU]) < 2:
                        if len(cellsWallingDict[(i,j)]) < 2:
                            newWall = ((i, j), (i, j+1))
                            if neighborU in cellsWallingDict and "down" not in cellsWallingDict[neighborU]: 
                                cellsWallingDict[neighborU].append("down")
                            if "up" not in cellsWallingDict[(i,j)]:
                                cellsWallingDict[(i,j)].append("up")
                else:
                    if neighborL not in cellsWallingDict or len(cellsWallingDict[neighborL]) < 2:
                        if len(cellsWallingDict[(i,j)]) < 2:
                            newWall = ((i, j), (i+1, j))
                            if neighborL in cellsWallingDict and "right" not in cellsWallingDict[neighborL]: 
                                cellsWallingDict[neighborL].append("right")
                            if "left" not in cellsWallingDict[(i,j)]:
                                cellsWallingDict[(i,j)].append("left")

                if newWall != None:
                    listOfWalls.append(newWall)

    return listOfWalls, goal











