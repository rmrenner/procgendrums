# DENNIS is the 4th draft of a generative music script
# for the Korg Volca Beats.

import mido
import time
import random
import NameGen

#----START CLASS DEFS

# An instance of instrument stores the midi message
# necessary to make the instrument sound
# and a table describing the probability that the instrument will sound
class Instrument:
	def __init__(self, name, midiVal, pTable):
		self.msg = mido.Message('note_on', note=midiVal,velocity=127,channel=9)
		self.pTable = pTable
		self.name = name

	def __str__(self):
		return self.name


# An instance of Pattern takes an Instrument
# And generates a pattern based on the instrument.
class Pattern:
	def __init__(self, inst):
		#save instrument
		self.instrument = inst
		#generate pattern
		self.pattern = []
		for i in self.instrument.pTable:
			x = random.randint(1,8)
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
		v.patterns = random.sample(self.patterns, random.randint(2, len(self.patterns)))
		return v


#-----START DATA DEFS

# Define instrument midi values
kick = Instrument("kick", 0x24, [8,0,0,1,4,0,1,1,6,0,3,1,4,1,2,1])
snare = Instrument("snare", 0x26, [0,0,0,0,7,0,0,1,1,3,0,0,7,0,1,1])
lotom = Instrument("lo tom", 0x2b, [0,1,2,2,0,1,2,2,0,2,1,3,2,1,5,1])
hitom = Instrument("hi tom", 0x32, [0,0,2,1,0,0,0,3,2,4,1,3,0,0,1,0])
clhat = Instrument("cl hat", 0x2a, [4,2,7,3,4,3,7,3,4,2,6,2,4,2,5,2])
ophat = Instrument("op hat", 0x2e, [0,0,1,0,0,0,1,1,0,1,3,0,0,0,1,0])
clap = Instrument("clap", 0x27, [0,0,0,1,4,0,1,0,2,0,1,1,5,0,1,0])
claves = Instrument("claves", 0x4b, [1,2,3,2,3,3,3,2,3,1,1,5,2,1,2,1])
agogo = Instrument("agogo", 0x43, [1,0,3,0,1,2,2,2,1,1,2,1,1,1,3,1])
crash = Instrument("crash", 0x31, [1,2,1,3,1,1,3,1,1,2,1,2,1,1,3,2])

scriptName = "DENNIS"

# Instrument sets:
instExtended = [lotom, hitom, clap, claves, agogo]
instStripped = [kick, snare, clhat, ophat]
#instSet = instStripped + random.sample(instExtended, random.randint(0,len(instExtended)))
instSet = instStripped + instExtended

# Set song title.
title = NameGen.generate()

#set tempo
tempo = random.randint(90,140)

#Set number of unique bars
uniqueBars = 2

#Set number of variations to play on those bars
variations = random.randint(10, 16)

#Set number of repetitions for each variation.
repeats = 4

p = mido.open_output(u'mio')

bars = []

#Generate bars
for i in range(uniqueBars):
	bars.append(Bar(instSet))

#Playback!
print("{} presents \"{}\".".format(scriptName, title))
print("{} is now playing {} variations on {} unique bars at a tempo of {}BPM.".format(scriptName, variations, uniqueBars,tempo))
print(scriptName + " is employing the following instruments for this composition: " + ', '.join(map(str, instSet)))
# Do the following four times:
# Iterate through each bar
# Generate a variation on that bar
# Play that variation four times
for i in range(variations):
	for b in bars:
		v = b.getVariant()
		for i in range(repeats):
			v.play(p, tempo)
