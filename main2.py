#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:42:05 2021

@author: Joshua Atienza, Janet Zhang
@net-id: jra165, jrz42
@project: Minesweeper
"""

import numpy as np
import sys    
import random

class Cell:
    def __init__(self, coord):
        self.coord = coord

        #status 0:covered, 1:bomb, clue:safe
        self.status = 0
        self.safeNeighbors = []
        self.mineNeighbors = []
        self.hiddenNeighbors = []
        return 
    def __str__(self):
        nodestr="My index value is {}, my space is a mine? {}, I am covered? {}, I am surrounded by {} mines, I am surrounded by {} safe squares, I have identified {} mines, I am surrounded by {} hidden squares, they have indices of {}."
        return nodestr.format(self.index, self.status, self.status, self.clue, len(self.safeCells), len(self.foundMines), len(self.hidden),self.hidden)


#ENVIRONMENT STUFF


d = int(sys.argv[1]) 
n = int(sys.argv[2])

env = np.zeros((d,d))
mineLocations = []

minesadded = 0

while minesadded != n:
    x = random.randint(0, d-1)
    y = random.randint(0, d-1)
    if env[x][y] == -1: 
        continue
    env[x][y] = -1
    mineLocations.append([x,y])
    minesadded +=1 

directions = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1], [-1,1], [1,-1]]

for mine in mineLocations:
    x = mine[0]
    y = mine[1]
    for i in range(len(directions)):
        a = x + directions[i][0]
        b = y + directions[i][1]
        if(a < 0 or b < 0 or a >= d or b >= d
            or env[a][b] == -1):
            continue
        env[a][b] += 1
    


### AGENT STUFF


aTracker = np.ndarray((d,d), dtype= Cell)
for x in range(d):
    for y in range(d):
        aTracker[x][y] = Cell([x,y])

#Simple Agent SETUP
minesMarked = []
minesExploded = []
cellsSafe = []
cellsHidden = []
cellsExplored = []
for x in range(d):
    for y in range(d):
        cellsHidden.append(aTracker[x][y].coord)
#Simple Agent SOLVE
while len(cellsHidden)!=0:
    x = random.randint(0, d-1)
    y = random.randint(0, d-1)
    clue = env[x][y]
    agentCell = aTracker[x][y]
    #if randomly found bomb
    if(clue == -1):
        minesExploded.append([x,y])
        minesMarked.append([x,y])
        cellsHidden.remove([x,y])
        agentCell.status = clue
        break
    else:
        cellsSafe.append([x,y])
        cellsHidden.remove([x,y])
        agentCell.status = clue
        if(clue - len(agentCell.mineNeighbors) == len(agentCell.hiddenNeighbors)):
            for h in range(len(agentCell.hiddenNeighbors)):   # for all hidden neighbors
                if((agentCell.hiddenNeighbors[h] not in minesMarked)):    # if the mine is not ID'd
                    cellsHidden.remove(agentCell.hiddenNeighbors[x])   # remove mine from unsearched
                    minesMarked.append(agentCell.hiddenNeighbors[x])      # append mine to ID mines
                for x in range(d):
                    for y in range(d):                 # for all nodes in the field - remove ranspace node from hidden node list of each node
                        if agentCell.coord in aTracker[x][y].hiddenNeighbors:
                            aTracker[x][y].hiddenNeighbors.remove(agentCell.coord)
            #ranspace.Hidden.clear() # no more hidden nodes in ranspace
        elif(clue - agentCell.minesMarked - len(agentCell.safeNeighbors) == len(agentCell.hiddenNeighbors)): 
            for i in range(len(agentCell.hiddenNeighbors)):       # for all hidden neighbors
                    if(agentCell.hiddenNeighbors[i] not in cellsSafe):         # if neighbor index is not in safe
                        cellsSafe.append(agentCell.hiddenNeighbors[i])         # add neighbor index to 
                        aTracker[x][y]
            agentCell.hiddenNeighbors.clear()    
        

        break
for x in range(d):
    for y in range(d):   
        print(aTracker[x][y].status, end =" ")
    print('')

#• If, for a given cell, the total number of mines (the clue) minus the number of revealed mines is the number of
#  hidden neighbors, every hidden neighbor is a mine.
#• If, for a given cell, the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors is
#  the number of hidden neighbors, every hidden neighbor is safe.
#• If a cell is identified as safe, reveal it and update your information.
#• If a cell is identified as a mine, mark it and update your information.
#• The above steps can be repeated until no more hidden cells can be conclusively identified.
#• If no hidden cell can be conclusively identified as a mine or safe, pick a cell to reveal uniformly at random from
#  the remaining cells.


