# CARMEN is a variant on CONNIE that uses a different set of drum patterns as source material.

#These were scraped from some "Latin" FPC drum patterns in FLStudio. They ended up only using three instruments and didn't have enough variation to produce interesting results.

import mido
import time
import random

#----START CLASS DEFS

# An instance of Instrument stores the midi message necessary to make the instrument sound and a table describing the probability that the instrument will sound
class Instrument:
	def __init__(self, midiVal, pTable):
		self.msg = mido.Message('note_on', note=midiVal,velocity=127,channel=9)
		self.pTable = pTable

# An instance of Pattern takes an Instrument
# And generates a pattern based on the instrument.
class Pattern:
	def __init__(self, inst):
		#save instrument
		self.instrument = inst
		#generate pattern
		self.pattern = []
		for i in self.instrument.pTable:
			x = random.randint(1,12)
			if (x <= i):
				self.pattern.append(True)
			else:
				self.pattern.append(False)

# An instance of bar takes a list of instruments
# And generates a list of patterns that can be played in sync
class Bar:
	def __init__(self, instrumentSet):
		self.patterns = []
		for i in instrumentSet:
			self.patterns.append(Pattern(i))

	# plays patterns through port at specified tempo
	def play(self, port, tempo):
		#calc time to sleep between steps:
		hexnote = 60.0 / (tempo * 4)
		# count through the steps of the patterns
		for i in range(16):
			# look through each pattern
			for p in self.patterns:
				if (p.pattern[i]):
					port.send(p.instrument.msg)
			#sleep a bit before hitting next step
			time.sleep(hexnote)

	# returns a new bar with a random subset of the patterns
	def getVariant(self):
		#Make new bar with a null set of instruments; we'll provide our own.
		v = Bar([])
		v.patterns = random.sample(self.patterns, random.randint(1, len(self.patterns)))
		return v


#-----START DATA DEFS

# Define instrument midi values
kick = Instrument(0x24, [12,0,0,0,12,0,0,12,0,4,0,2,8,0,0,2])
snare = Instrument(0x26, [2,0,12,0,0,12,0,0,0,6,6,2,0,10,2,0])
#lotom = Instrument(0x2b, [0,1,2,2,0,1,2,2,0,2,1,3,2,1,5,1])
#hitom = Instrument(0x32, [0,0,2,1,0,0,0,3,2,4,1,3,0,0,1,0])
clhat = Instrument(0x2a, [5,0,6,6,6,6,0,6,6,3,3,6,5,6,1,5])
#ophat = Instrument(0x2e, [0,0,1,0,0,0,1,1,0,1,3,0,0,0,1,0])
#clap = Instrument(0x27, [0,0,0,1,4,0,1,0,2,0,1,1,5,0,1,0])
#claves = Instrument(0x4b, [1,2,3,2,3,3,3,2,3,1,1,5,2,1,2,1])
#agogo = Instrument(0x43, [1,0,3,0,1,2,2,2,1,1,2,1,1,1,3,1])
#crash = Instrument(0x31, [1,2,1,3,1,1,3,1,1,2,1,2,1,1,3,2])

# Instrument sets:
#instFull = [kick, snare, lotom, hitom, clhat, ophat, clap, claves, agogo]
#instStripped = [kick, snare, clhat, ophat]
instFPCLatin = [kick, snare, clhat]
#set tempo
tempo = 156

#Set number of unique bars
uniqueBars = 6

p = mido.open_output(u'mio')

bars = []

#Generate bars
for i in range(uniqueBars):
	bars.append(Bar(instFPCLatin))

#Playback!

# Do the following four times:
# Iterate through each bar
# Generate a variation on that bar
# Play that variation four times

for i in range(4):
	for b in bars:
		v = b.getVariant()
		for i in range(2):
			v.play(p, tempo)
