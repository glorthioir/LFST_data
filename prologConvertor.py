#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 14:14:52 2018

@author: guillaume

prologConvertor.py contains function to convert ILP 2016 instructions in a map
"""

import random

def euclideanDistance(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def dataExtraction(file):
    tmpW = []
    walls = []
    paths = []
    path = []
    f = open(file ,'r')
    
    for line in f:
        if line[0:8] !="agent_at" and path != []:
            paths.append(path)
            path = []
            
        pos = line.find('(')
        
        if pos != -1:
            word = line[0:pos]
            
            if word == "wall":
                commaPos = line.find(',')
                endPos = line.find(')')
                commaPos2 = line.find(',',endPos+2)
                endPos2 = line.find(')', endPos+2)
            
                if commaPos == -1 or endPos == -1 or commaPos2 == -1 or endPos2 == -1:
                    continue
                else:
                    wall = ((int(line[pos+2:commaPos]), int(line[commaPos+1:endPos])), (int(line[endPos+3:commaPos2]), int(line[commaPos2+1:endPos2])))
                    tmpW.append(wall)
                    
            elif word == "agent_at":
                commaPos = line.find(',')
                endPos = line.find(')')
                
                if commaPos == -1 or endPos == -1 or line.find('(', pos+1) == -1:
                    continue
                else:
                    direction = (int(line[pos+2:commaPos]),int(line[commaPos+1:endPos]))
                    path.append(direction)    

    if len(path) >0:
        paths.append(path)                                
            
    for elem in tmpW:
        x1, y1, x2, y2 = 0, 0, 0, 0
        
        if elem[0][0] < elem[1][0]:
            x1 = elem[1][0]
            y1 = elem[0][1]
            x2 = x1
            y2 = y1+1
        elif elem[0][0] > elem[1][0]:
            x1 = elem[0][0]
            y1 = elem[0][1]
            x2 = x1
            y2 = y1+1
        elif elem[0][1] > elem[1][1]:
            x1 = elem[0][0]
            y1 = elem[0][1]
            x2 = x1+1
            y2 = y1
        elif elem[0][1] < elem[1][1]:
            x1 = elem[0][0]
            y1 = elem[1][1]
            x2 = x1+1
            y2 = y1
        
        wall = ((x1, y1), (x2, y2))
        if wall != ((0, 0), (0, 0)) and wall not in walls:
            walls.append(wall)
            
    f.close()
    
    return walls, paths


def dataWriter(file, walls, transitions, width, height, goalPosition):    # where transition it's a couple (position, action) 
    #noWalls = len(walls) == 0
    noWalls = False
    f = open(file ,'w')
    line = "VAR pos"
    
    for i in range(width*height):
        line += " "+str(i)
            
    f.write(line)
    
    line = "\nVAR move l u r d s"
    f.write(line)
    line = ""
    
    if not noWalls:
        line += "\nVAR leftW 0 1"
        line += "\nVAR upW 0 1"
        line += "\nVAR rightW 0 1"
        line += "\nVAR downW 0 1"
        
    line += "\nVAR closer 0 1 2"    # 0 for farther, 1 if equal and 2 if closer 
    line += "\nVAR goal 0 1"
    
    #line = "\nVAR behavior 1 2 3"
    
    #line += "\n"
    f.write(line)
    
    journeysList = []
    
    for transition in transitions:
        
        newDist = 0
        previousState = {} 
        statesList = []
        
        for state in transition:
            
            leftW = 0
            upW = 0
            rightW = 0
            downW = 0
            closer = 1
            goal = 0
            prevDist = newDist
            newDist = euclideanDistance(state[0], goalPosition)
            pos = state[0][1]*width + state[0][0]
            
            if state[0] == goalPosition:
                goal = 1
            else:
                goal = 0
                    
            if prevDist < newDist and len(previousState) > 0:
                closer = 0
            elif prevDist == newDist or len(previousState) == 0:
                closer = 1
            else:
                closer = 2
                    
            for wall in walls:
                if wall[0][1] == wall[1][1]:
                    if wall[0][1] == state[0][1] and state[0][0] >= min(wall[0][0], wall[1][0]) and state[0][0] < max(wall[0][0], wall[1][0]):
                        upW = 1
                    elif wall[0][1] == state[0][1]+1 and state[0][0] >= min(wall[0][0], wall[1][0]) and state[0][0] < max(wall[0][0], wall[1][0]):
                        downW = 1
                        
                if wall[0][0] == wall[1][0]:
                    if wall[0][0] == state[0][0] and state[0][1] >= min(wall[0][1], wall[1][1]) and state[0][1] < max(wall[0][1], wall[1][1]):
                        leftW = 1
                    elif wall[0][0] == state[0][0]+1 and state[0][1] >= min(wall[0][1], wall[1][1]) and state[0][1] < max(wall[0][1], wall[1][1]):
                        rightW = 1
                    
            if len(previousState) > 0:
                
                line = "\npos="+str(previousState["pos"])+" move="+previousState["move"]
                
                if not noWalls:
                    line += " leftW="+str(previousState["leftW"])+" upW="+str(previousState["upW"])+" rightW="+str(previousState["rightW"])+" downW="+str(previousState["downW"])
                
                line += " closer="+str(previousState["closer"])
                line += " goal="+str(previousState["goal"])
                line += " : pos="+str(pos)
                line += " move="+state[1]
                
                if not noWalls:
                    line += " leftW="+str(leftW)+" upW="+str(upW)+" rightW="+str(rightW)+" downW="+str(downW)
                    
                line += " closer="+str(closer)
                line += " goal="+str(goal)
                f.write(line)
                          
            previousState["pos"] = pos
            previousState["move"] = state[1]
            
            if not noWalls:
                previousState["leftW"] = leftW
                previousState["upW"] = upW
                previousState["rightW"] = rightW
                previousState["downW"] = downW
                
            previousState["closer"] = closer
            previousState["goal"] = goal
            
            statesList.append(dict(previousState))
        
        journeysList.append(statesList)
    
    f.close()
    
    return journeysList
             

def removeVarGoal(res):
    newRes = []
    
    for elem in res:
        for key in elem:   
            
            if key == "goal":
                elem.pop(key)    
                break
            
        if len(elem) > 0 and elem not in newRes:
            newRes.append(dict(elem))
            
    return newRes
            
            
def traceCleaning(variablesToRemove, traces):
    newTraces = []
    
    for trace in traces:
        
        newTrace = []
        for elem in trace:

            newDict = dict(elem)
            for key in elem:   

                if key in variablesToRemove:
                    newDict.pop(key)   

            newTrace.append(dict(newDict))
                
        newTraces.append(list(newTrace))
            
    return newTraces


def convertorTracesExamples(originalTraces):
    traces = list(originalTraces)
    positiveExamples = []
    negativeExamples = []
    
    for path in traces:
        for state in path:

            goalState = state["goal"]
            state.pop("goal")
            
            if goalState == 1:
                positiveExamples.append(state)
                break
            else:
                negativeExamples.append(state)
                
    return positiveExamples, negativeExamples

            
def csvFileWriter(positiveExamples, negativeExamples, file):
    f = open(file ,'w')
    line = ""
    textBuffer = []

    for word in positiveExamples[0]:
        line += str(word)+ ','

    line += "Decision\n"
    f.write(line)

    for positive in positiveExamples:
        line = ""

        for word in positive:
            line += str(positive[word]) + ','

        line += "Yes\n"
        textBuffer.append(line)

    for negative in negativeExamples:
        line = ""

        for word in negative:
            line += str(negative[word]) + ','

        line += "No\n"
        textBuffer.append(line)

    size = len(textBuffer)
    for i in range(size):
        line = textBuffer.pop(random.randint(0, len(textBuffer)-1))
        f.write(line)

    f.close()


def saveResForTable(file, percentList, lfstAc, mgiAc, c45Ac, lfstRe, mgiRe, c45Re, environment):
    f = open(file ,'w')
    line = "Result for the Environment : "+environment+'\n'
    f.write(line)

    line =" & Accuracy & Recall \\\\ \n"
    f.write(line)
    f.write("\\hline\n")

    line ="Percentage of missing data & LFST & C4.5 & MGI & LFST & C4.5 & MGI \\\\ \n"
    f.write(line)
    f.write("\\hline\n")

    for n in range(len(percentList)):
        line = str(round(percentList[n]))+' & '+str(round(lfstAc[n], 2))+' & '+str(round(c45Ac[n], 2))+' & '+str(round(mgiAc[n], 2))+' & '+str(round(lfstRe[n], 2))\
        +' & '+str(round(c45Re[n], 2))+' & '+str(round(mgiRe[n], 2))+"\\\\ \n"
        f.write(line)
        f.write("\\hline\n")

    f.close()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            