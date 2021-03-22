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

        self.clue = 0

        self.agentsMines = 0

        self.neighborsSafe = []

        self.neighborsHidden = []

        self.neighborsAll = []
        
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
    while mine_count != n:
        temp = random.randrange(d**2)
        if(field[temp].isMine == False):
            field[temp].isMine = True
            mine_count = mine_count + 1
    
    #Add information to each cell in the field
    for i in range(d**2):
        
        add_knowledge(field, field[i], d)
        field[i].neighborsHidden.extend(field[i].neighborsAll)
        
    return field

#Prints the field
def print_field(field, d):
    
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
This function is intended for providing all the necessary information about each cell in the field
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
                    cell.clue += 1
                cell.neighborsAll.append(index - d)
            elif(move == "south"):
                if field[index + d].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index + d)
            elif(move == "west"): 
                if field[index - 1].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index - 1)
            elif(move == "east"):
                if field[index + 1].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index + 1)
            elif(move == "north-west"):
                if field[index - d - 1].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index - d - 1)
            elif(move == "north-east"):
                if field[index - d + 1].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index - d + 1)
            elif(move == "south-west"):
                if field[index + d - 1].isMine == True:
                    cell.clue += 1
                cell.neighborsAll.append(index + d - 1)
            elif(move == "south-east"):
                if field[index + d + 1].isMine == True:
                    cell.clue += 1  
                cell.neighborsAll.append(index + d + 1)  
        
    return directions 


"""
Code for our basic agent
"""
def simpleAgent(field, dim):

    # The Agent's information about the environment
    minesMarked = []
    minesExploded = []
    cellsSafe = []
    cellsHidden = []
    cellsExplored = []

    # Initialize the Agent's knowledge
    for x in range(len(field)):
        cellsHidden.append(field[x].index)

    # Explore the entire environment
    while(len(cellsHidden)!= 0 or len(cellsSafe) != 0):     

        # If there are known safe moves, explore those first
        if(len(cellsSafe) > 0):
            agentIndex = cellsSafe.pop()
            agentCell = field[agentIndex]
            cellsHidden.remove(agentIndex)

        # If no safe moves, make a random move. 
        else:
            agentIndex = random.randrange(len(cellsHidden))
            agentCell = field[cellsHidden[agentIndex]]
            cellsHidden.pop(agentIndex)

        # If random move was a mine, update Agent knowledge
        if(agentCell.isMine == True):
            minesExploded.append(agentCell.index)             
            for x in range(len(agentCell.neighborsAll)):
                field[agentCell.neighborsAll[x]].agentsMines += 1
                field[agentCell.neighborsAll[x]].neighborsHidden.remove(agentCell.index)


        # If random move was not a mine, check for the conditions that the Simple Agent recognizes
        else:
            cellsExplored.append(agentCell.index)

            #   If, for a given cell, the total number of mines (the clue) minus the number of revealed mines is the number of
            #   hidden neighbors, every hidden neighbor is a mine.
            if(agentCell.clue - agentCell.agentsMines == len(agentCell.neighborsHidden)):
                
                for x in range(len(agentCell.neighborsHidden)):
                    if((agentCell.neighborsHidden[x] not in minesMarked)):
                        cellsHidden.remove(agentCell.neighborsHidden[x])
                        minesMarked.append(agentCell.neighborsHidden[x])
                    
                    # Increase mine count
                    cell = field[agentCell.neighborsHidden[x]]
                    for i in range(len(cell.neighborsAll)):
                        field[cell.neighborsAll[i]].agentsMines += 1
                        
                    for y in range(len(field)):
                        if agentCell.neighborsHidden[x] in field[y].neighborsHidden and y != agentCell.index:
                            field[y].neighborsHidden.remove(agentCell.neighborsHidden[x])
                
                # neighbors have been revealed
                agentCell.neighborsHidden.clear()
            
            #   If, for a given cell, the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors 
            #   is the number of hidden neighbors, every hidden neighbor is safe.
            elif(len(agentCell.neighborsAll) - agentCell.clue - len(agentCell.neighborsSafe) == len(agentCell.neighborsHidden)):
                
                for x in range(len(agentCell.neighborsHidden)):
                    if(agentCell.neighborsHidden[x] not in cellsSafe):
                        cellsSafe.append(agentCell.neighborsHidden[x])
                        
                # neighbors have been revealed        
                agentCell.neighborsHidden.clear()

            # Reveal the cell: remove it from it's neighbors' hidden array and add it to known safe cells 
            for x in range(len(agentCell.neighborsAll)):
                
                if(agentCell not in field[agentCell.neighborsAll[x]].neighborsSafe):
                    field[agentCell.neighborsAll[x]].neighborsSafe.append(agentCell)
                    
                if len(field[agentCell.neighborsAll[x]].neighborsHidden) != 0:
                    if(agentCell.index in field[agentCell.neighborsAll[x]].neighborsHidden):
                        field[agentCell.neighborsAll[x]].neighborsHidden.remove(agentCell.index)


        print_info(field, dim, cellsHidden, cellsSafe, minesMarked, minesExploded, cellsExplored)
       
    return minesMarked, minesExploded


"""
Print all relevant information
"""
def print_info(field, dim, cellsHidden, cellsSafe, minesMarked, minesExploded, cellsExplored):
    
    print("Hidden cells are: " + str(cellsHidden))
    print("Safe cells are: " + str(cellsSafe))
    print("Marked mines are " + str(minesMarked))
    print("Exploded mines are: " + str(minesExploded))
    print("Explored cells are: " + str(cellsExplored))
    print("\n")
    print("Field: ")
    print_field(field, dim)
    
    

"""
Code for advanced agent
"""
def advAgent(field, dim):
    
    # The Agent's information about the environment
    minesMarked = []
    minesExploded = []
    cellsSafe = []
    cellsHidden = []
    cellsExplored = []
    
    #Create a dictionary of booleans, indicating whether or not a cell is "Done"
    isDone = [False] * len(field)
    
    # Initialize the Agent's knowledge
    for x in range(len(field)):
        cellsHidden.append(field[x].index)
    
    
    # Explore the entire environment
    while(len(cellsHidden) != 0 or len(cellsSafe) != 0):
        
        #Make a random move
        if(len(cellsSafe) == 0):
            
            ranindex = random.randrange(len(cellsHidden))      
            agentCell = field[cellsHidden[ranindex]]            
            cellsHidden.pop(ranindex)
            
        #Choose a known safe cell    
        elif(len(cellsSafe) > 0):                            

            ranindex = cellsSafe.pop(0)                        
            agentCell = field[ranindex]     

            #If chosen cell in Hidden, remove                    
            if(ranindex in cellsHidden):
                cellsHidden.remove(ranindex)               

        # If random move was a mine, update Agent knowledge
        if(agentCell.isMine == True):
            minesExploded.append(agentCell.index)             
            for x in range(len(agentCell.neighborsAll)):
                field[agentCell.neighborsAll[x]].agentsMines += 1
                
                #Remove condition
                if(agentCell.index in field[agentCell.neighborsAll[x]].neighborsHidden):
                    field[agentCell.neighborsAll[x]].neighborsHidden.remove(agentCell.index)
            
                    
        # If random move was not a mine, check for the conditions that the Simple Agent recognizes
        else:
        
            cellsExplored.append(agentCell.index)
            
            #  If, for a given cell, the total number of mines (the clue) minus the number of revealed mines is the number of
            #  hidden neighbors, every hidden neighbor is a mine.
            if(agentCell.clue - agentCell.agentsMines == len(agentCell.neighborsHidden)):
                
                for x in range(len(agentCell.neighborsHidden)):
                    
                    #If mine is not marked, remove from cellsHidden list, and add to minesMarked
                    if((agentCell.neighborsHidden[x] not in minesMarked)):
                        cellsHidden.remove(agentCell.neighborsHidden[x])
                        minesMarked.append(agentCell.neighborsHidden[x])
                        isDone[agentCell.neighborsHidden[x]] = True
                    
                    #Increase mine count
                    cell = field[agentCell.neighborsHidden[x]]
                    for i in range(len(cell.neighborsAll)):
                        field[cell.neighborsAll[i]].agentsMines += 1
                    
                    # remove agentCell from cellsHidden
                    for y in range(len(field)):                 
                        if agentCell.neighborsHidden[x] in field[y].neighborsHidden and y != agentCell.index:
                            field[y].neighborsHidden.remove(agentCell.neighborsHidden[x])
                
                #neighbors have been revealed
                agentCell.neighborsHidden.clear()
            
            #   If, for a given cell, the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors 
            #   is the number of hidden neighbors, every hidden neighbor is safe.
            elif(len(agentCell.neighborsAll)-agentCell.clue-len(agentCell.neighborsSafe)==len(agentCell.neighborsHidden)):
                for x in range(len(agentCell.neighborsAll)):
                    
                    if(agentCell.neighborsAll[x] not in cellsSafe and (not isDone[agentCell.neighborsAll[x]])):
                        cellsSafe.append(agentCell.neighborsAll[x])
                        
                agentCell.neighborsHidden.clear()
                
            for x in range(len(agentCell.neighborsAll)):
                
                if (agentCell not in field[agentCell.neighborsAll[x]].neighborsSafe) :
                    field[agentCell.neighborsAll[x]].neighborsSafe.append(agentCell)
                    
                if len(field[agentCell.neighborsAll[x]].neighborsHidden) != 0:
                    if(agentCell.index in field[agentCell.neighborsAll[x]].neighborsHidden):
                        field[agentCell.neighborsAll[x]].neighborsHidden.remove(agentCell.index)
        

        # Run only if we have extracted all information from a given cell
        if(len(agentCell.neighborsAll) - agentCell.agentsMines - len(agentCell.neighborsSafe) == 0 or agentCell.isMine):
            
            #Set a cell to Done if we have extracted all information from it
            temp = agentCell.index
            if(temp in cellsExplored):
                cellsExplored.remove(temp)
            if(temp in cellsSafe):
                cellsSafe.remove(temp)
            isDone[temp] = True
            
            # Add explored cells to safe, eliminating duplicates with set
            cellsSafe = list(set().union(cellsExplored, cellsSafe))
            cellsExplored.clear()
        
        #Run if we do not know all information about a given cell
        else:
            
            temp = []
            for x in range(len(cellsExplored)):
                
                #
                cell = cellsExplored[x]
                if (len(field[cell].neighborsAll)-field[cell].clue - len(field[cell].neighborsSafe) == len(field[cell].neighborsHidden) 
                    or field[cell].clue - field[cell].agentsMines == len(field[cell].neighborsHidden)):
                    temp.append(cell)
                    cellsSafe.append(cell)
        
            for y in range(len(temp)):
                cellsExplored.remove(temp[y])
                
        #Print all relevant information about the current state of the field        
        print_info_advanced(field, dim, cellsHidden, cellsSafe, minesMarked, minesExploded, cellsExplored, isDone)
          
    return minesMarked, minesExploded

"""
Print all relevant information
"""
def print_info_advanced(field, dim, cellsHidden, cellsSafe, minesMarked, minesExploded, cellsExplored, isDone):
    
    print("Hidden cells are: " + str(cellsHidden))
    print("Safe cells are: " + str(cellsSafe))
    print("Marked mines are " + str(minesMarked))
    print("Exploded mines are: " + str(minesExploded))
    print("Explored cells are: " + str(cellsExplored))
    print("isDone cells are: " + str(isDone))
    print("\n")
    print("Field: ")
    print_field(field, dim)       

def main():

    mazefield =[]
    dim = 8
    mineTotal = 10
    iterations = 1
    advanced= []
    simple=[]
    mines=[]
    t=time.time()
    for x in range(iterations):
        mazefield = generate_field(dim,mineTotal)
        mazefieldCopy = copy.deepcopy(mazefield)
        mazefieldMineCount = copy.deepcopy(mazefield)
        #minesdetected=simpleAgent(mazefield,dim)
        minesdetected2=advAgent(mazefieldCopy,dim)
        #advanced.append(minesdetected2)

if __name__ == "__main__":
    main()
