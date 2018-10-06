'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 21:00 (EST) Fri 10/05/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@last_update: Modelled the flatworm

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
  
  blockwidth = 20
  blocklength = 48
  coords = [(i-j/2, j-k/2, k) for i in range(0,blockwidth) for j in range(0,blocklength) for k in range(0,4)]
  widths = [2, 5, 6, 9, 10, 13, 14, 17, 18, 19, 16, 15, 12, 11, 10, 11, 12, 13, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 13, 12, 13, 12, 11, 10, 11, 10, 9, 8, 9, 8, 7, 6, 5, 4, 3, 2, 0]
  # Add agents to board
  for c in coords:
    if (c[0] + (c[1]+1)/2 - blockwidth/2)**2 <= (widths[c[1]]/2)**2 and (widths[c[1]] % 2 == 1 or (c[0] + (c[1]+1)/2 - blockwidth/2) <= (widths[c[1]]/2)-1):
        b.addAgent(c)
      
  # Initialize plotting
  mpl.interactive(True)
  p = plot3dClass()
  # Cycle program
  for j in range(20):
    for i in b.getAllAgents():
      sense(b,i,3,4,0.5)
      newPacket(b, i, 5)
    for i in b.getAllAgents():
      act(b,i)
    noPacks = 0
    for i in b.getAllAgents():
      noPacks = noPacks + len(i.ReceivedPackets)
    print "Number of packets:" +  `noPacks`
  p.drawNow(board_2_coords(b))

  if raw_input() == "cut":
    cutPos = int(raw_input())
    for i in b.getAllAgents():
        if cutPos > blocklength/2 and i.i_id[1] >= cutPos or cutPos <= blocklength/2 and i.i_id[1] <= cutPos:
            b.removeAgent(i.i_id)
  p.drawNow(board_2_coords(b))
  raw_input()
  for j in range(10):
    x = int(raw_input())
    for k in range(x):
        for i in b.getAllAgents():
          sense(b,i,3,4,0.5)
          newPacket(b, i, 5)
        for i in b.getAllAgents():
          act(b,i)
    p.drawNow(board_2_coords(b))
