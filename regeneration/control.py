'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 07:10 (EST) Sun 09/28/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@last_update: Small test "organism" made 

@description: control.py pulls together objects and functions from both
engine.py and visuals.py, alongside a possible network class to control
and complete the models explored in the HRILab's papers on tissue regeneration.
'''

from engine import *
from visuals import*
from random import randint, seed
import matplotlib as mpl

seed(1337)

if __name__ == "__main__":
  
  # Create 5x5x5 board
  b = board_engine(100,100,10)
  
  # Find agents for 3x3x3 organism
  coords = [(i,j,k) for i in range(10,15) for j in range(10,15) for k in range(10,14)]
  
  # Add agents to board
  for c in coords:
    b.addAgent(c)
    
  # Add packets to board
  for i in range(1):
      #Random position
      p = (randint(10,14),
           randint(10,14),
           randint(10,14))
      
      #Random direction
      d = b.relatives[randint(0,11)]
      
      #Assign packet to given agent
      b.getAgentAtPosition(p).ReceivedPackets.append(Packet(d))
      
  # Initialize plotting
  mpl.interactive(True)
  p = plot3dClass()
  
  # Cycle program
  for j in range(100):
    for i in b.getAllAgents():
      sense(b,i,3,4,0.5)
    for i in b.getAllAgents():
      act(b,i)
    p.drawNow(board_2_coords(b))
