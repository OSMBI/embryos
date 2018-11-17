'''
@created: 13:17 (EST) Sun 07/29/2018

@last_modified: 22:00 (EST) Fri 11/14/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@last_update: Modelled the flatworm

@description: control.py pulls together objects and functions from both
engine.py and visuals.py, alongside a possible network class to control
and complete the models explored in the HRILab's papers on tissue regeneration.
'''

from engine import *
from visuals import *
from random import randint, seed
import matplotlib as mpl

seed(1337)

if __name__ == "__main__":
  
  minvec = 1
  toplen = 1
  bendprob = 0.2
  deathprob = 0.04
  packetFreq = 1
  
  # Create a board
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
  for j in range(80):
    for i in b.getAllAgents():
      sense(b,i,minvec,toplen,bendprob)
      newPacket(b, i, packetFreq)
      act(b,i)
    noPacks = 0
    for i in b.getAllAgents():
      noPacks = noPacks + len(i.ReceivedPackets)
    print `j` + " Number of packets:" +  `noPacks`
  p.drawNow(board_2_coords(b))
  
  raw_input()
  cellnumber = 525*4
  for j in range(420):
    livingcells = 0;
    for i in b.getAllAgents():
        if rand.uniform(0,1) < deathprob:
            b.removeAgent(i.i_id)
            continue
        sense(b,i,minvec,toplen,bendprob)
        newPacket(b, i, packetFreq)
        act(b,i)
    for c in coords:
        if (c[0] + (c[1]+1)/2 - blockwidth/2)**2 <= (widths[c[1]]/2)**2 and (widths[c[1]] % 2 == 1 or (c[0] + (c[1]+1)/2 - blockwidth/2) <= (widths[c[1]]/2)-1):
            if b.getAgentAtPosition(c) != None:
                livingcells = livingcells+1
    fractionAlive = livingcells/float(cellnumber)
    print `livingcells` + "/" + `cellnumber` + "=" + `fractionAlive`
    if fractionAlive < 0.9:
        print "Dead."
        break
    
  p.drawNow(board_2_coords(b))
  raw_input()
'''  cutting functionality commented out:
if raw_input() == "cut":
    cutPos = int(raw_input())
    for i in b.getAllAgents():
        if cutPos > blocklength/2 and i.i_id[1] >= cutPos or cutPos <= blocklength/2 and i.i_id[1] <= cutPos:
            b.removeAgent(i.i_id)
  p.drawNow(board_2_coords(b))
  raw_input()
  for j in range(100):
    x = int(raw_input())
    for k in range(x):
        for i in b.getAllAgents():
          sense(b,i,minvec,toplen,bendprob)
          act(b,i)
    p.drawNow(board_2_coords(b))'''
