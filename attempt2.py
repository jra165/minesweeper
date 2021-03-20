import random
import math
import queue
import copy
import time

class Node:
    def __init__(self,index):
        self.index = index
        self.isMine = False #init
        self.isCovered = True
        self.numMines=0 
        self.SafeSquares=[] 
        self.numIdMines=[]
        self.Hidden=[] #init
        self.Neighbors =[] #init
        return 

# Creates the environment using Nodes
def createField(dim,mines):
    field=[]
    count=0
    # Add new Cell to field list 
    for x in range(dim**2):
        tempnode=Node(x)
        field.append(tempnode)
    # Randomly assign mines to cells
    while count < mines:
        temp=random.randrange(dim**2)
        if(field[temp].isMine == False):
            field[temp].isMine = True
            count = count+1
    # TENTATIVE: Checks and assigns all valid neighbors
    for x in range(dim**2):
        neighborinfo=checkneighbors(field,field[x],dim)
        field[x].Hidden.extend(field[x].Neighbors)
    return field


def checkneighbors(field,node,dim):
    index=node.index
    dimension=dim
    possibleMoves = [True, True, True, True, True, True, True, True] # up, down, left, right, up-left, up-right, down-left, down-right
    topLCorner = 0
    topRCorner = dimension - 1 
    col = index%dimension 
    # Check for maze boundary conditions
    if (index - dimension < topLCorner): # top edge
        possibleMoves[0] = False
    if (index + dimension > topRCorner): #bottom edge
        possibleMoves[1] = False
    if (col == 0): # leftmost col
        possibleMoves[2] = False
    if (col == dimension-1): # rightmost col
        possibleMoves[3] = False
    if (possibleMoves[0] & possibleMoves[2] == False):
        possibleMoves[4] = False
    if (possibleMoves[0] & possibleMoves[3] == False):
        possibleMoves[5] = False
    if (possibleMoves[1] & possibleMoves[2] == False):
        possibleMoves[6] = False
    if (possibleMoves[1] & possibleMoves[3] == False):
        possibleMoves[7] = False

    # For all the directions
    for x in range(len(possibleMoves)):
        # If it's a valid movement
        if(possibleMoves[x] == True):
            # If the direction is upwards
            if(x==0):
                # If upwards is a Mine
                if(field[index-dim].isMine == True):
                    # Increase the Cell's number of known mines
                    node.numMines=node.numMines+1
                # Add the index upwards Cell to the current Cell's neighbors
                node.Neighbors.append(index-dim)
            # Downwards direction
            elif(x==1):
                if field[index+dim].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index+dim)
            # Cell to the left 
            elif(x==2): 
                if field[index-1].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index-1)
            # Cell to the right
            elif(x==3):
                if field[index+1].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index+1)
            # Cell to the up-left
            elif(x==4):
                if field[index-dim-1].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index-dim-1)
            # Cell to the up-right
            elif(x==5):
                if field[index-dim+1].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index-dim+1)
            # Cell to the  down-left
            elif(x==6):
                if field[index+dim-1].isMine == True:
                    node.numMines=node.numMines+1
                node.Neighbors.append(index+dim-1)
            # Cell to the down-right
            elif(x==7):
                if field[index+dim+1].isMine == True:
                    node.numMines=node.numMines+1  
                node.Neighbors.append(index+dim+1) 
    return possibleMoves 



def printfield(field,dimension):
    print("\n")
    total = 0
    for num in range(dimension):
        for i in range(dimension):
            if(field[total+i].isMine == True):
                print ("M", end=" ")
            else:
                print ("0", end=" ") #print number
        print("\n")
        total+=(dimension)


def simpleAgent(field,dim):
    idmines=[]
    expmines=[]
    safe=[]
    unsearched=[]
    explored=[]
    for x in range(len(field)):
        unsearched.append(field[x].index)
    
    while(len(safe)!=0 or len(unsearched)!=0):      # if there are still safe nodes or unsearched nodes]

        # Move made when forced to choose random cell
        if(len(safe)== 0):                              # path if no more safe nodes
            ranindex=random.randrange(len(unsearched))      # get random index from unsearched and assign to ranindex
            ranspace=field[unsearched[ranindex]]            # use random index to get node
            unsearched.pop(ranindex)                        # remove index from unsearched
            field[ranspace.index].isCovered=False           # reveal the node
            # print("Current Node")
            # print(ranspace.index,"\n",len(unsearched))
        
        # Revealing known safe cells
        elif(len(safe) > 0):                            # path if still safe nodes
            ranindex=safe.pop(0)                        # get first index on safe list
            ranspace=field[ranindex]                    # use index to get safe node
            if ranindex in unsearched:
                unsearched.remove(ranindex)                 # remove safe node from unsearched
            field[ranindex].isCovered=False             # reveal the node
            # print("Current Node")
            # print(ranindex,"\n",len(unsearched))

        # If randomly selected a mine, update environment Cell by removing from Hidden property and adding index to numIdMines
        if(ranspace.isMine == True):                    # path if node selected from random is a mine
            expmines.append(ranspace.index)             
            for x in range(len(ranspace.Neighbors)):
                field[ranspace.Neighbors[x]].numIdMines.append(ranspace.index)
                if ranspace.index in field[ranspace.Neighbors[x]].Hidden:
                    field[ranspace.Neighbors[x]].Hidden.remove(ranspace.index)

        # Randomly selected a safe cell
        #address neighbors when removing
        elif(ranspace.isMine == False):                 # path if node selected is not a mine
            explored.append(ranspace.index)             # add node index to explored
            if(ranspace.numMines - len(ranspace.numIdMines) == len(ranspace.Hidden)): # every node is a mine around it
                for x in range(len(ranspace.Hidden)):   # for all hidden neighbors
                  #  print(ranspace.Hidden)
                    if((ranspace.Hidden[x] not in idmines)):    # if the mine is not ID'd
                        if ranspace.Hidden[x] in unsearched:
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
        printfield(env, 6)
        #for z in range(len(field)):
            #print(field[z])
    return len(idmines)

def minedetect(field,node):
    for x in range(len(node.Neighbors)):
        field[node.Neighbors[x]].numIdMines.append(node.index)





env = createField(6, 6)
simpleAgent(env, 6)
