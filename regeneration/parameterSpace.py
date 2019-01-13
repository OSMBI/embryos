class ParameterSpace:
	def __init__(self, d):
		self.deathProb = 0
		self.packetFreq = 0
		self.minBends = 0
		self.minTopLen = 0
		self.bendProb = 0

		if d != None:
			for a,b in d.items():
				setattr(self, a, obj(b) if isinstance(b, dict) else b)
