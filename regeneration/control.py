'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 10:04 (EST) Sun 09/25/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@last_update: Small test "organism" made 

@description: control.py pulls together objects and functions from both
engine.py and visuals.py, alongside a possible network class to control
and complete the models explored in the HRILab's papers on tissue regeneration.
'''

from engine import *
from visuals import*
from time import sleep

if __name__ == "__main__":
  
  # Create 5x5x5 board
  b = board_engine(5,5,5)
  
  # Find agents for 3x3x3 organism
  coords = [(i,j,k) for i in range(1,4) for j in range(1,4) for k in range(1,4)]
  
  # Add agents to board
  for c in coords:
    b.addAgent(c)
    
  # Initialize plotting
  fig,ax = init_plot()
  
  # Cycle program
  while True:
    for i in b.getAllAgents():
      sense(b,i,3,4,0.5)
      act(b,i)
      iter_plot(b,fig,ax)
      break
    break
