'''
@created: 12:04 (ECT) Wed 01/09/2018

@last_modified: 12:04 (ECT) Wed 01/09/2018

@authors: LB

@institution: Open-Source Mathematical Biology Initiative (OSMBI)

@description: Dynamically creates worms with different simulation parameters to create meaningful statistics for paper result reproduction.
'''

from engine import *
from visuals import *
from random import randint, seed

# Shape of a single layer as looked from above
# use this shape for newer papers
#shape = [2, 5, 6, 9, 10, 13, 14, 17, 18, 19, 16, 15, 12, 11, 10, 11, 12, 13, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 13, 12, 13, 12, 11, 10, 11, 10, 9, 8, 9, 8, 7, 6, 5, 4, 3, 2, 0]
# use this shape for the oldest paper
shape = [0, 1, 8, 9, 10, 11, 12, 13, 14, 15, 14, 15, 16, 15, 14, 13, 12, 13, 12, 11, 10, 11, 10, 9, 8, 9, 10, 11, 12, 9, 6, 5, 2]

blockwidth = max(shape)+1
blocklength = len(shape)

# Amount of layers every worm has
layers = 4

# Total amount of cells for every worm
cellnumber = sum(shape)*layers;

# Amount of cycles until we start adding cell death events
precycles = 80

# Amount of cycles where celldeath is simulated until the worm is declared to survive
livingcycles = 120

seed(1337)

def executeSimulation(minvec, toplen, bendprob, deathprob, packetFreq): 
    b = board_engine(100, 100, 10)
    coords = [(i-j/2, j-k/2, k) for i in range(0,blockwidth) for j in range(0,blocklength) for k in range(0,layers)]
    
    cellMold = [c for c in coords if CellExistsInMold(c)]
    
    # Add agents to board
    for c in cellMold:
        b.addAgent(c)

    ### Worm is now completely instantiated.

    # Start by filling worm with packets before simulating cell death 
    for j in range(precycles):
        for i in b.getAllAgents():
            sense(b, i, minvec, toplen, bendprob)
            newPacket(b, i, packetFreq)
            act(b,i)
        print `j`

    # Simulate cell death
    for j in range(livingcycles):
        livingCells = 0
        for i in b.getAllAgents():
            if rand.uniform(0,1) < deathprob:
                b.removeAgent(i.i_id)
                continue
            sense(b,i,minvec,toplen,bendprob)
            newPacket(b,i,packetFreq)
            act(b,i)
            if CellExistsInMold(i.i_id):
                livingCells += 1
        fractionAlive = livingCells/float(cellnumber)
        print `fractionAlive` + " " + `livingCells` + "/" + `cellnumber`
        if fractionAlive < 0.9:
            print "Dead"
            break
    print "Simulation end"

# returns if there should be a cell at the given position
def CellExistsInMold(c):
    return (c[0] + (c[1]+1)/2 - blockwidth/2)**2 <= (shape[c[1]]/2)**2 and (shape[c[1]] % 2 == 1 or (c[0] + (c[1]+1)/2 - blockwidth/2) <= (shape[c[1]]/2)-1)

if __name__ == "__main__":
    executeSimulation(1,1,0.2,0.04,1)
