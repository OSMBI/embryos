'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 15:08 (EST) Sun 08/11/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@description: engine.py component contains class constructions of agent and packets as well as
functions used in Algorithms 1 and 2 as described in the paper "dynamic structure discovery
and repair for 3d cell assemblages (2016)" by Mike Levin et al.

@last_update: engine.py now parses, finishing touches made to allow workable model in
control.py.
'''

import numpy as np
import random as rand
from random import randint


def tuple_add(a,b):
    return tuple(map(sum,zip(a,b)))

#camelCase XOR underscores boys!
class board_engine:
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
        relatives = [(1,0,0),(-1,0,0),(0,1,0),
                     (0,-1,0),(0,0,1),(0,0,-1),
                     (1,-1,0),(-1,1,0),(1,0,-1),
                     (-1,0,1),(0,1,-1),(0,-1,1)]
                
        return [tuple_add(position,rel) for rel in relatives] #if self.board[tuple_add(position,rel)] != None]
        
    # Returns the list of neighbouring agents from a given position
    def getNeighbouringAgents(self,position):
        neighbourCoordinates = self.getNeighbouringCoordinates(position)
        return [self.board[pos[0],pos[1],pos[2]] for pos in neighbourCoordinates if self.board[pos[0],pos[1],pos[2]] != None]
        
    def getFilledCoordinates(self,position):
        neighbourCoordinates = self.getNeighbouringCoordinates(position)
        return [pos for pos in neighbourCoordinates if self.board[pos[0],pos[1],pos[2]] != None]
        
    def getAllAgents(self):
      temp = self.board.flatten()
      return [agent for agent in temp if agent != None]
        
    # This kills a cell/agent, i.e. Removes it from the given position
    def removeAgent(self, agentPosition):
        self.board[agentPosition[0], agentPosition[1], agentPosition[2]] = None
        
    # This generates a new cell/agent at the given position, if there is no agent at that place yet
    def addAgent(self,agentPosition):
        if self.board[agentPosition[0], agentPosition[1], agentPosition[2]] == None:
            #print(self.getNeighbouringAgents(agentPosition))
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
    ReceivedPackets = [] #list of packets recived from neighbors
    HeldPackets = [] #list of packets cell is holding 
    sendingPackets = [] #list of packets cell is sending
    
    def __init__(self,pos):
        self.i_id = (pos[0],pos[1],pos[2]) #cell position in board
        
    def __str__(self):
        return "Agent located at %s" % self.i_id #nice string to print

class Packet:
    # Communication packet that is sent between cells to statistically save structural information

    directions = []
    bends = 0
    steps = []
    backtracking = False
    
    def __init__(self, direction_vector):
        self.directons.append(direction_vector)
        
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
        # If the packet is backtracking, check if it finished backtracking in that direction and if so, drop the top direction.
        if self.backtracking and self.steps[-1] <= 0:
                self.steps.pop()
                self.directions.pop()
        return [-j if self.backtracking else j for j in self.directions[-1]] # reverses direction if backtracking

    # decrements the amount of steps for the current vector if backtracking or
    # increments it if not
    def step(self):
        if self.backtracking:
            self.steps[-1] -= 1
        else:
            self.steps[-1] += 1
            
    def distance(self):
      return self.steps[-1]
        
def sense(board,i,minvec,toplen,bendprob):
    for packetbeta in i.ReceivedPackets:
      top = packetbeta.getDirection() #pop out 
      if not packetbeta.backtracking:
        top.Distance += 1
      else:
        if packetbeta.Bends >= minvec and packetbeta.distance > toplen and board.getAgentAtPosition[tuple_add(i.i_id,top.direction)] != None:
          i.HeldPackets.append(packetbeta)
        elif rand.uniform(0,1) <= bendprob: #returns random var from uniform distribution
          packetbeta.bend(board.getNewDirection(top.direction,i.i_id))
      i.sendingPackets.append(packetbeta)
            
def reverse(beta):
  return [-b for b in beta] #does this make sense in axial? yes.            

def act(board,i):
    for packetbeta in i.sendingPackets:
      top = packetbeta.getDirection()
      if board.getAgentAtPosition[tuple_add(i.i_id,top)] != None: # if the destination neighbor is alive...
       # i.sendPacket(top, packetbeta) # send the packet in that direction
        board.getAgentAtPosition[tuple_add(i.i_id,top)].ReceivedPackets.append(packetbeta)
        packetbeta.step()
      else: # if agent at that position isnt alive
        packetbeta.bend(packetbeta.getNewDirection(board,top.direction,i.i_id))
    i.sendingPackets = [] # clears sendingPackets list