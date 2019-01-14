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
import socket
import json
from parameterSpace import *

TCP_IP = '88.99.224.205'
TCP_PORT = 5005
BUFFER_SIZE = 1024

# Shape of a single layer as looked from above
# use this shape and layers for newer papers
#shape = [2, 5, 6, 9, 10, 13, 14, 17, 18, 19, 16, 15, 12, 11, 10, 11, 12, 13, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 13, 12, 13, 12, 11, 10, 11, 10, 9, 8, 9, 8, 7, 6, 5, 4, 3, 2, 0]
#layers = 4
# use this shape and layers for the oldest paper
shape = [0, 1, 8, 9, 10, 11, 12, 13, 14, 15, 14, 15, 16, 15, 14, 13, 12, 13, 12, 11, 10, 11, 10, 9, 8, 9, 10, 11, 12, 9, 6, 5, 2]
layers = 8

blockwidth = max(shape)+1
blocklength = len(shape)

# Total amount of agents for every worm
numberOfAgents = sum(shape)*layers;

# Amount of cycles until we start adding agent death events (80 in paper)
precycles = 80

# Amount of cycles where celldeath is simulated until the worm is declared to survive (420 in paper)
livingCycles = 420

# Amount of simulations done for a single parameter space (8 in paper)
simulsPerParameterSpace = 8

# Number of agents for suvival (0.9*numberOfAgents in paper)
minAgents = 0.9*numberOfAgents

seed(time.clock())

# Executes the simulation, returns the number of cycles above threshold
def executeSimulation(minvec, toplen, bendprob, deathprob, packetFreq): 
    b = board_engine(100, 100, 10)
    coords = [(i-j/2, j-k/2, k) for i in range(0,blockwidth) for j in range(0,blocklength) for k in range(0,layers)]
    
    agentMold = [c for c in coords if agentExistsInMold(c)]
    
    # Add agents to board
    for c in agentMold:
        b.addAgent(c)

    ### Worm is now completely instantiated.

    print "Simulating precycle"
    # Start by filling worm with packets before simulating agent death 
    for j in range(precycles):
        for i in b.getAllAgents():
            sense(b, i, minvec, toplen, bendprob)
            newPacket(b, i, packetFreq)
            act(b,i,0)


    print "Simulating death..."
    # Simulate agent death
    for j in range(livingCycles):
        livingAgents = numberOfAgents
        for i in b.getAllAgents():
            if rand.uniform(0,1) < deathprob:
                b.removeAgent(i.i_id)
                livingAgents -= 1
                if livingAgents < minAgents:
                    print "Dead at " + `j`
                    return j+1
                continue
            sense(b,i,minvec,toplen,bendprob)
            newPacket(b,i,packetFreq)
            act(b,i,livingAgents)

    print "Organism survived"
    return j+1

# returns if there should be a agent at the given position
def agentExistsInMold(c):
    return (c[0] + (c[1]+1)/2 - blockwidth/2)**2 <= (shape[c[1]]/2)**2 and (shape[c[1]] % 2 == 1 or (c[0] + (c[1]+1)/2 - blockwidth/2) <= (shape[c[1]]/2)-1)


while 1:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send("jobreq")
	data = s.recv(BUFFER_SIZE)
	s.close()

	print data
	try:
		parameterSpace = ParameterSpace(json.loads(data))
		print parameterSpace
		simulResults = []
		startTime = time.clock()
		for i in range(simulsPerParameterSpace):
		    x = executeSimulation(parameterSpace.minBends,parameterSpace.minTopLen,parameterSpace.bendProb,parameterSpace.deathProb,parameterSpace.packetFreq)
		    simulResults.append(x)
	
		parameterSpace.simulResults = simulResults
	
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
		s.send(json.dumps(parameterSpace.__dict__))
		s.close
	except Exception as e:
		print e
