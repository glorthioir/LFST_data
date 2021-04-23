import random
import operator
import itertools
from collections import Counter


from Agent import * 
from prologConvertor import *




def euclideanDistance(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])




def behaviorsAnalyse(world, walls, height, width, paths):
    possibilities = []
    actions = []
    
    for path in paths:
        action = ['s']
        previousState = path[0]
        
        for state in path[1:len(path)]:
            
            distance = euclideanDistance(previousState, state)
            direction = ""
            throughWall = False
            
            if distance > 0:
                
                if state[0] > previousState[0]:
                    direction += "right_"
                    action.append('r')
                if state[0] < previousState[0]:
                    direction += "left_"
                    action.append('l')
                if state[1] < previousState[1]:
                    direction += "up_"
                    action.append('u')
                if state[1] > previousState[1]:
                    direction += "down_"
                    action.append('d')                    
                    
                for wall in walls:
                    if direction.find("right_") != -1:
                        if wall[0][0] == wall[1][0] and wall[0][0] == previousState[0]+1 and (previousState[1] <= wall[0][1] and previousState[1] >= wall[1][1] or previousState[1] >= wall[0][1] and previousState[1] <= wall[1][1]): 
                            throughWall = True
                            break
                    elif direction.find("down") != -1:
                        if wall[0][1] == wall[1][1] and wall[0][1] == previousState[1]+1 and (previousState[0] <= wall[0][0] and previousState[0] >= wall[1][0] or previousState[0] >= wall[0][0] and previousState[0] <= wall[1][0]): 
                            throughWall = True
                            break
                    elif direction.find("left") != -1:
                        if wall[0][0] == wall[1][0] and wall[0][0] == previousState[0] and (previousState[1] <= wall[0][1] and previousState[1] >= wall[1][1] or previousState[1] >= wall[0][1] and previousState[1] <= wall[1][1]): 
                            throughWall = True
                            break
                    elif direction.find("up") != -1:
                        if wall[0][1] == wall[1][1] and wall[0][1] == previousState[1] and (previousState[0] <= wall[0][0] and previousState[0] >= wall[1][0] or previousState[0] >= wall[0][0] and previousState[0] <= wall[1][0]): 
                            throughWall = True
                            break        
                    
            else:
                direction += "stay_"
                action.append('s')
                
            possibility = "distance_"+str(distance)+"_"+direction
            if throughWall:
                possibility+="wall_"
                
            if possibility not in possibilities:
                possibilities.append(possibility)
            
            previousState = state
        
        actions.append(action)
            
    return possibilities, actions