'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 21:00 (EST) Fri 10/05/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@description: engine.py component contains class constructions of agent and packets as well as
functions used in Algorithms 1 and 2 as described in the paper "dynamic structure discovery
and repair for 3d cell assemblages (2016)" by Mike Levin et al.

@last_update: Fixed some bugs that werent apparent until the flatworm actually regenerated.
Speaking of regenerating function, thars what I added too.
'''

import numpy as np
import random as rand
from random import randint


def tuple_add(a,b):
    return tuple(map(sum,zip(a,b)))

#camelCase XOR underscores boys!
class board_engine:
    relatives = [(1,0,0),(-1,0,0),(0,1,0),
                 (0,-1,0),(0,0,1),(0,0,-1),
                 (1,-1,0),(-1,1,0),(1,0,-1),
                 (-1,0,1),(0,1,-1),(0,-1,1)]
#container class that handles the coordinate system and has an overview over each agent and its position.
    def __init__(self,BOARD_SIZE_X,BOARD_SIZE_Y,BOARD_SIZE_Z):
        BOARD_SIZE_X = 500 # just an arbitrary number I set, may have to be higher. 
        BOARD_SIZE_Y = 500 # just an arbitrary number I set, may have to be higher. 
        BOARD_SIZE_Z = 20 # just an arbitrary number I set, may have to be higher. (Smaller than the others since we have a *flat* worm, duh
        
        # contains the address of the agent in the angent list at every point in our coordinate system, or none if no agent lives there
        self.board = np.full((BOARD_SIZE_X,BOARD_SIZE_Y,BOARD_SIZE_Z), None)
        
        # this is the actual list of cells.
        self.agents = [] 
    
    # Returns the agent at that specific location or None if there is none
    def getAgentAtPosition(self,position):
        return self.board[position[0],position[1],position[2]]
    
    # Returns the list of coordinates that are neighbouring the given position
    # Note: This does not check for overflow because of limited board size yet
    def getNeighbouringCoordinates(self,position):                
        return [tuple_add(position,rel) for rel in self.relatives] #if self.board[tuple_add(position,rel)] != None]
        
    # Returns the list of neighbouring agents from a given position
    def getNeighbouringAgents(self,position):
        neighbourCoordinates = self.getNeighbouringCoordinates(position)
        return [self.board[pos[0],pos[1],pos[2]] for pos in neighbourCoordinates if self.board[pos[0],pos[1],pos[2]] != None]
    
    # Returns all coordinates with agents
    def getFilledCoordinates(self,position):
        neighbourCoordinates = self.getNeighbouringCoordinates(position)
        return [pos for pos in neighbourCoordinates if self.board[pos[0],pos[1],pos[2]] != None]
    
    # Returns a list of all agents
    def getAllAgents(self):
        temp = self.board.flatten()
        return [agent for agent in temp if agent != None]
        
    # This kills a cell/agent, i.e. Removes it from the given position
    def removeAgent(self, agentPosition):
        self.board[agentPosition[0], agentPosition[1], agentPosition[2]] = None
        
    # This generates a new cell/agent at the given position, if there is no agent at that place yet
    def addAgent(self,agentPosition):
        if self.board[agentPosition[0], agentPosition[1], agentPosition[2]] == None:
            self.board[agentPosition[0], agentPosition[1], agentPosition[2]] = agent(agentPosition)
    
    # Finds new direction for a wayward packet
    def getNewDirection(self,direction,i_id): 
        valid_neighbors = self.getFilledCoordinates(i_id)
        valid_neighbors.pop(direction)
        valid_neighbors.pop(-direction)
        if len(valid_neighbors) == 0:
              return direction
        return valid_neighbors[randint(0,len(valid_neighbors))].i_id

class agent:
    
    def __init__(self,pos):
        self.i_id = (pos[0],pos[1],pos[2]) #cell position in board
        self.ReceivedPackets = [] #list of packets recived from neighbors
        self.HeldPackets = [] #list of packets cell is holding 
        self.sendingPackets = [] #list of packets cell is sending
    
    def __str__(self):
        return "Agent located at %s" % str(self.i_id) #nice string to print

class Packet:
    # Communication packet that is sent between cells to statistically save structural information
    
    def __init__(self, direction_vector):
        #Some exceptions to avoid strange aimless packets
        if type(direction_vector) != tuple:
            raise Exception('direction_vector must of tuple type!')
        if len(direction_vector) != 3:
            raise Exception('direction_vector must be a 3-tuple!')
        self.directions = [direction_vector]
        self.bends = 0
        self.steps = [0]
        self.backtracking = False
        
    # Adds a new bend in the packet, i.e. a new direction that is appended after the last one.
    def bend(self, direction_vector):
        self.directions.append(direction_vector)
        self.steps.append(0)
        self.bends += 1
        
    # Sets backtracking as True. So far, its not required to set backtracking to False again, as packets that finished backtracking get purged.
    def backtrack(self):
        self.backtracking = True
    
    # Returns top vector on the direction stack or 
    # if the packet is backtracking, return the top vector on the direction stack reversed
    def getDirection(self):
        return tuple([-j if self.backtracking else j for j in self.directions[-1]]) # reverses direction if backtracking
    
    # Get new random direction different from current direction
    def getNewDirection(self,board,i_id):
        
        #Random direction
        d = board.relatives[randint(0,11)]
        #Select a direction that has an agent and is not the original direction
        while (len(self.directions) > 0 and self.getDirection() == d) or board.getAgentAtPosition(tuple_add(i_id,d)) == None:
            d = board.relatives[randint(0,11)]
        return d
    
    # decrements the amount of steps for the current vector if backtracking or
    # increments it if not
    def step(self):
        if self.backtracking:
            self.steps[-1] -= 1
        else:
            self.steps[-1] += 1
            
    def distance(self):
        try:
            return sum(self.steps)
        except IndexError:
            return

        
def sense(board,i,minvec,toplen,bendprob):
    for packetbeta in i.ReceivedPackets:
        i.ReceivedPackets.remove(packetbeta)
        if packetbeta.steps[-1] <= 0 and packetbeta.backtracking:
            packetbeta.steps.pop()
            packetbeta.directions.pop()
            if packetbeta.directions == []:
                break
        if packetbeta.bends >= minvec and packetbeta.distance > toplen:
            packetbeta.backtrack()
        elif rand.uniform(0,1) <= bendprob: #returns random var from uniform distribution
            packetbeta.bend(packetbeta.getNewDirection(board,i.i_id))
        i.sendingPackets.append(packetbeta)

      
      
def newPacket(board, i, packetFreq):
    for x in range (0, packetFreq):
        i.sendingPackets.append(Packet(board.relatives[randint(0,11)]))
            
def reverse(beta):
  return [-b for b in beta] #does this make sense in axial? yes.            

def act(board,i):
    for packetbeta in i.sendingPackets:
        try:
            top = packetbeta.getDirection()
        except:
            print(vars(packetbeta))
        if board.getAgentAtPosition(tuple_add(i.i_id,top)) != None: # if the destination neighbor is alive...
            board.getAgentAtPosition(tuple_add(i.i_id,top)).ReceivedPackets.append(packetbeta)
            packetbeta.step()
        else: # if no agent at direction proposed
            if not packetbeta.backtracking:
                if packetbeta.steps[-1]==0:
                    packetbeta.steps.pop()
                    packetbeta.directions.pop()
                packetbeta.bend(packetbeta.getNewDirection(board,i.i_id))
                top = packetbeta.getDirection()
                board.getAgentAtPosition(tuple_add(i.i_id,top)).ReceivedPackets.append(packetbeta)
                packetbeta.step()
            else:
                board.addAgent(tuple_add(i.i_id,top))
                board.getAgentAtPosition(tuple_add(i.i_id,top)).ReceivedPackets.append(packetbeta)
                packetbeta.step()
    i.sendingPackets = [] # clears sendingPackets list
