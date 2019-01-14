#!/usr/bin/env python

import json
import socket
import time
import random
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

JOB_TIMEOUT = 48*3600 # how much time until a job is pruned (in case it was accepted by a client that is no longer active)
PRUNE_FREQUENCY = 60 # delay between executions of the prune function.

SIMUL_OUT_FILE = "simulations.txt"

AMOUNT_OF_SIMULS = 50688

deathProbs = [0.01, 0.02, 0.03, 0.04]
packetFreqs = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
minBendss = [1, 3, 5, 7]
minTopLens = [1, 3, 5, 7]
bendProbs = [0.2, 0.3, 0.4, 0.5,  0.6, 0.7, 0.8, 0.9, 1.0]

class ParameterSpace:
	def __init__(self, d):
		self.deathProb = 0
		self.packetFreq = 0
		self.minBends = 0
		self.minTopLen = 0
		self.bendProb = 0
		if d != None:
			for a, b in d.items():
				setattr(self, a, obj(b) if isinstance(b, dict) else b)

class Job:
	def __init__(self):
		self.jobId = 0
		self.timeStamp = 0

def getParameterSpace(n):
	a = ParameterSpace(None)
	a.deathProb = deathProbs[n%4]
	n /= 4
	a.packetFreq = packetFreqs[n%11]
	n /= 11
	a.minBends = minBendss[n%4]
	n /= 4
	a.minTopLen = minTopLens[n%4]
	n /= 4
	a.bendProb = bendProbs[n%9]
	return a

def getParameterSpaceId(parameterSpace): # This is probably insanely slow and risky, maybe send the id inside the json?
	n = bendProbs.index(parameterSpace.bendProb)
	n *= 4
	n += minTopLens.index(parameterSpace.minTopLen)
	n *= 4
	n += minBendss.index(parameterSpace.minBends)
	n *= 11
	n += packetFreqs.index(parameterSpace.packetFreq)
	n *= 4
	n += deathProbs.index(parameterSpace.deathProb)
	return n

print getParameterSpaceId(getParameterSpace(5124))

# deletes old jobs from joblist and adds them back into the todo list
def pruneOldJobs():
	print "Pruning old jobs"
	currTime = time.time()
	for job in jobs:
		if currTime - job.timeStamp > JOB_TIMEOUT: # older than one day...
			jobs.remove(job)
			simulsToDo.append(job.jobId)
	threading.Timer(PRUNE_FREQUENCY, pruneOldJobs).start()

simulsToDo = range(0, AMOUNT_OF_SIMULS-1)
jobs = []

with open(SIMUL_OUT_FILE) as simulEntries:
	for line in simulEntries:
		try:
			simulsToDo.remove(int(line.split(":")[0]))
		except:
			print "Warning: malformatted line"
	simulEntries.close()
random.shuffle(simulsToDo)
print simulsToDo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

pruneOldJobs()

while 1:
	conn, addr = s.accept()
	print 'Connection address: ', addr
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print "received data:", data
		if data == "jobreq":
			if len(simulsToDo) == 0:
				continue

			x = simulsToDo.pop()
			conn.send(json.dumps(getParameterSpace(x).__dict__))
			job = Job()
			job.jobId = x
			job.timeStamp = time.time()
			jobs.append(job)
		else:
			try:
				simulResult = ParameterSpace(json.loads(data))
				parameterSpaceId = getParameterSpaceId(simulResult)
				with open(SIMUL_OUT_FILE, "a") as outfile:
					outfile.write(`parameterSpaceId`+": "+`simulResult.__dict__`+"\n")
					outfile.close()
				for i, job in enumerate(jobs):
					if job.jobId == parameterSpaceId:
						del jobs[i]
						break
				print "Received results for job " + `parameterSpaceId`
			except Exception as e:
				print e
	conn.close()
