#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 18:49:26 2021

@author: joshua.atienza
"""

import random
import math
import queue
import copy
import time

class Cell:
    
    def __init__(self, index):
        self.index = index

        self.isMine = False

        self.isCovered = True

        self.numMines = 0

        self.SafeSquares = []

        self.numIdMines = []

        self.Hidden = []

        self.Neighbors = []
        
"""
Code for generating the mine field
We create a list of cells, where their associated index correlates to the position in the dxd mine field
"""
def generate_field(d, n):
    
    #Initialize field and count of mines
    field = []
    mine_count = 0
    
    #Add a new cell in the range
    for i in range(d**2):
        cell = Cell(i)
        field.append(cell)
        
    #Randomly generate a mine in a given cell, increase count
    for i in range(n):
        temp = random.randrange(d**2)
        if(field[temp].isMine == False):
            field[temp].isMine = True
            mine_count = mine_count + 1
    
    #Add information to each cell in the field
    for i in range(d**2):
        add_knowledge(field, field[i], d)
        field[i].Hidden.extend(field[i].Neighbors)
        
    return field

#Prints the field
def print_field(field,d):
    print("\n")
    total = 0
    for num in range(d):
        for i in range(d):
            if(field[total+i].isMine == True):
                print ("M", end=" ")
            else:
                print ("0", end=" ") #print number
        print("\n")
        total += d
        
"""
Checks the possible moves to make in every direction
Add information about the neighbors of a given cell, and increase number of mines if necessary
"""
def add_knowledge(field, cell, d):
    
    #Initialize variables
    index = cell.index
    dimension = d
    column = index % dimension
    left_corner = 0
    bottom_corner = dimension**2 - 1
    
    #Dictionary of possible cardinal, ordinal directions of mine
    #Initialize them to true
    directions = {
        
        "north": True,
        "south": True,
        "west": True,
        "east": True,
        "north-west": True,
        "north-east":True,
        "south-west": True,
        "south-east": True
        
    }

    #Check possible moves for top-left corner (first index) and bottom-right corner (last index)
    if (index - dimension < left_corner):
        directions["north"] = False
    if (index + dimension > bottom_corner):
        directions["south"] = False
        
    #Check possible moves for leftmost and rightmost columns
    if (column == 0):
        directions["west"] = False
    if (column == dimension-1):
        directions["east"] = False
        
    #Check possibly moves in the ordinal directions
    if (directions["north"] & directions["west"] == False):
        directions["north-west"] = False
    if (directions["north"] & directions["east"] == False):
        directions["north-east"] = False
    if (directions["south"] & directions["west"] == False):
        directions["south-west"] = False
    if (directions["south"] & directions["east"] == False):
        directions["south-east"] = False

    # Loop through all the possible directions to update the number of mines
    # and neighbors for valid moves
    for move in directions.keys():
        
        #Update the values of node for valid directional moves
        if(directions[move] == True):

            if(move == "north"):
                if(field[index - d].isMine == True):
                    cell.numMines += 1
                cell.Neighbors.append(index - d)
            elif(move == "south"):
                if field[index + d].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index + d)
            elif(move == "west"): 
                if field[index - 1].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index - 1)
            elif(move == "east"):
                if field[index + 1].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index + 1)
            elif(move == "north-west"):
                if field[index - d - 1].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index - d - 1)
            elif(move == "north-east"):
                if field[index - d + 1].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index - d + 1)
            elif(move == "south-west"):
                if field[index + d - 1].isMine == True:
                    cell.numMines += 1
                cell.Neighbors.append(index + d - 1)
            elif(move == "south-east"):
                if field[index + d + 1].isMine == True:
                    cell.numMines += 1  
                cell.Neighbors.append(index + d + 1)  
        
    return directions 


"""
Code for our basic agent
"""
def simpleAgent(field, dim):
    idmines=[]
    expmines=[]
    safe=[]
    unsearched=[]
    explored=[]
    for x in range(len(field)):
        unsearched.append(field[x].index)
    
    while(len(safe)!=0 or len(unsearched)!=0):      # if there are still safe nodes or unsearched nodes]
        if(len(safe)== 0):                              # path if no more safe nodes
            ranindex=random.randrange(len(unsearched))      # get random index from unsearched and assign to ranindex
            ranspace=field[unsearched[ranindex]]            # use random index to get node
            unsearched.pop(ranindex)                        # remove index from unsearched
            field[ranspace.index].isCovered=False           # reveal the node
            # print("Current Node")
            # print(ranspace.index,"\n",len(unsearched))
        elif(len(safe) > 0):                            # path if still safe nodes
            ranindex=safe.pop(0)                        # get first index on safe list
            ranspace=field[ranindex]                    # use index to get safe node
            unsearched.remove(ranindex)                 # remove safe node from unsearched
            field[ranindex].isCovered=False             # reveal the node
            # print("Current Node")
            # print(ranindex,"\n",len(unsearched))

        if(ranspace.isMine == True):                    # path if node selected from random is a mine
            expmines.append(ranspace.index)             
            for x in range(len(ranspace.Neighbors)):
                field[ranspace.Neighbors[x]].numIdMines.append(ranspace.index)
                field[ranspace.Neighbors[x]].Hidden.remove(ranspace.index)
        #address neighbors when removing
        elif(ranspace.isMine == False):                 # path if node selected is not a mine
            explored.append(ranspace.index)             # add node index to explored
            if(ranspace.numMines - len(ranspace.numIdMines) == len(ranspace.Hidden)): # every node is a mine around it
                for x in range(len(ranspace.Hidden)):   # for all hidden neighbors
                  #  print(ranspace.Hidden)
                    if((ranspace.Hidden[x] not in idmines)):    # if the mine is not ID'd
                        unsearched.remove(ranspace.Hidden[x])   # remove mine from unsearched
                        idmines.append(ranspace.Hidden[x])      # append mine to ID mines
                    minedetect(field,field[ranspace.Hidden[x]]) # pass neighbor into mine detect - mine detect tells all the mines neighbors, its been ID'd
                    for y in range(len(field)):                 # for all nodes in the field - remove ranspace node from hidden node list of each node
                        if ranspace.Hidden[x] in field[y].Hidden and y!=ranspace.index:
                            field[y].Hidden.remove(ranspace.Hidden[x])
                ranspace.Hidden.clear() # no more hidden nodes in ranspace
            elif(len(ranspace.Neighbors)-ranspace.numMines-len(ranspace.SafeSquares)==len(ranspace.Hidden)): # every node is safe around it
                for x in range(len(ranspace.Hidden)):       # for all hidden neighbors
                    if(ranspace.Hidden[x] not in safe):         # if neighbor index is not in safe
                        safe.append(ranspace.Hidden[x])         # add neighbor index to safe
                ranspace.Hidden.clear()                     # remove all neighbors from node's hidden
            for x in range(len(ranspace.Neighbors)):        # for all neighbors
                if(ranspace not in field[ranspace.Neighbors[x]].SafeSquares):
                    field[ranspace.Neighbors[x]].SafeSquares.append(ranspace)   # append original node to all neighbors safe spaces
                if len(field[ranspace.Neighbors[x]].Hidden) != 0:           # for all neighbors, remove original node from their hidden
                    if(ranspace.index in field[ranspace.Neighbors[x]].Hidden):
                        field[ranspace.Neighbors[x]].Hidden.remove(ranspace.index)
        print("Unsearched")
        for x in range(len(unsearched)):
            print(unsearched[x])
        print("safe")
        print(safe) 
        print("IdedMines")
        print(idmines)
        print('Exploded mines')
        print(expmines)
        print("Explored")
        print(explored)   
        print("current status")
        print_field(field, 3)
    return len(idmines)


def minedetect(field,node):
    for x in range(len(node.Neighbors)):
        field[node.Neighbors[x]].numIdMines.append(node.index)
def tilesolved(field,node):
    if(len(field[node].Neighbors)-field[node].numMines-len(field[node].SafeSquares)==len(field[node].Hidden)):
        return True
    elif(field[node].numMines - len(field[node].numIdMines) == len(field[node].Hidden)):
        return True
    else:
        return False

def main():

    mazefield =[]
    dim=3
    mineTotal=3
    iterations=1
    advanced= []
    simple=[]
    mines=[]
    t=time.time()
    for x in range(iterations):
        mazefield=generate_field(dim,mineTotal)
        mazefieldCopy = copy.deepcopy(mazefield)
        mazefieldMineCount=copy.deepcopy(mazefield)
        minesdetected=simpleAgent(mazefield,dim)

if __name__ == "__main__":
    main()
