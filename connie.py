# CONNIE is the 3rd draft of a generative music script
# for the Korg Volca Beats.

# CONNIE generates 2 unique bars of randomized music at the BPM specified by tempo
# Each bar contains 16 16th notes.

# The probability that an instrument i will sound at a given step t
# is based on how often i is triggered at time t in the eight factory preset patterns
# of the Volca Beats.

# CONNIE then loops through the generated bars in sequence 16 times.
# For each bar, it selects a non-empty subset of the instruments to be played.

# This is a hamfisted way of reproducing repetition and the dynamic
# ebb and flow of human-composed music.

import mido
import time
import random

#------SONG TITLE GENERATOR.
#		Might be worthwhile to put this in its own module

class NameFormat:
	def __init__(self, word_types, delimiter):
		self.word_types = word_types
		self.delimiter = delimiter

	def generate_title(self):
		words = []
		for c in self.word_types:
			s = random.choice(c)
			c.remove(s)
			words.append(s)
		return self.delimiter.join(words)

adjectives = ['Wet', 'Glamorous', 'Sexy', 'Urban', 'Helpless', 'Intimate', 'Mild', 'Fake', 'Dense', 'Morbid', 'Funny', 'Awful', 'Crisp', 'Cold', 'Hot', 'False', 'True', 'Young', 'Infinite', 'Shaky', 'Permanent', 'Ancient', 'Nasty', 'Sick', 'Delicate', 'Deep', 'Dry', 'Fuzzy', 'Long', 'Unique', 'Old', 'Electric', 'Healing', 'Redemptive', 'Effervescent', 'Ecstatic', 'Cute']
cloth_types = ['Satin', 'Cotton', 'Silk', 'Gingham', 'Burlap', 'Organza', 'Suede', 'Vinyl', 'Polyester', 'Denim']
colors = ['Black', 'White', 'Grey', 'Pink', 'Silver', 'Gold', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet']
garments = ['Shorts', 'Pants', 'Hotpants', 'Skirt', 'Miniskirt', 'Gown', 'Party Dress', 'Long-Sleeved Shirt', 'Short-Sleeved Shirt', 'Breeches', 'Tube Top', 'Jacket']
given_names = ['Amy', 'Jessica', 'Christina', 'Leona', 'Amber', 'Nancy', 'Nelda', 'Octavio','Perla', 'Yesenia', 'Sara', 'Mari', 'Jeff', 'Marcos', 'Peter', 'Roberto', 'Susana', 'Jose', 'Sean', 'Elke', 'Tamiko', 'Yuri', 'Oscar']
last_names = ['Enchi', 'Beckett', 'Calvino', 'Ochoa', 'Garza', 'Stein', 'Jefferson', 'Tanizaki', 'Ayala', 'Harris', 'Suleiman', 'Sandford', 'Hall', 'Puig']
nouns = ['Desire', 'Forest', 'Grace', 'Hate', 'Legend','Love', 'Mask','Milk','Murder','Poise','Problem', 'Shadow','Statesman', 'Cakes', 'Cookie', 'Quake', 'Stories', 'Box', 'Man', 'Morning', 'Magician', 'Tower', 'Genius', 'Beauty', 'Rifle', 'Decay', 'Game', 'Life', 'Day', 'Night', 'Guest', 'Girl', 'Face', 'Handbook', 'Diary', 'Justice', 'Crime', 'Thought', 'Warmth', 'Depth', 'Light', 'Seed', 'Swerve', 'Envy', 'Germs', 'Burn', 'Lips', 'Eyes', 'Midnight', 'Queen']

cnfs = [] #Company name formats. Each entry is a tuple containing a list and a string
cnfs.append(NameFormat([adjectives, adjectives], ' & ')) #Sexy & Fake
cnfs.append(NameFormat([adjectives, adjectives, adjectives], ', ')) #Helpless, Intimate, Mild
cnfs.append(NameFormat([adjectives, adjectives, nouns], ' ')) #Sexy Urban Love
cnfs.append(NameFormat([adjectives, cloth_types],' ')) #Mild Cotton
cnfs.append(NameFormat([adjectives, colors],' ')) #Helpless Gold
cnfs.append(NameFormat([adjectives, garments], ' ')) #Wet Hotpants
cnfs.append(NameFormat([adjectives, given_names], ' ')) #Glamorous Amy
cnfs.append(NameFormat([adjectives, nouns], ' ')) #Wet Problem

cnfs.append(NameFormat([cloth_types, garments],' ')) #Gingham Pants
cnfs.append(NameFormat([cloth_types, nouns],' ')) #Silk Mask

cnfs.append(NameFormat([colors, cloth_types],' ')) #Blue Gingham
cnfs.append(NameFormat([colors, cloth_types, garments],' ')) #Blue Gingham Pants
cnfs.append(NameFormat([colors, cloth_types, nouns],' ')) #Blue Gingham Forest
cnfs.append(NameFormat([colors, nouns],' ')) #Blue Love

cnfs.append(NameFormat([nouns, nouns], ' ')) #Forest Shadow
cnfs.append(NameFormat([nouns, nouns], ' of ')) #Forest of Shadow


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

# Instrument sets:
instExtended = [lotom, hitom, clap, claves, agogo, crash]
instStripped = [kick, snare, clhat, ophat]
#instSet = instStripped + random.sample(instExtended, random.randint(0,len(instExtended)))
instSet = instStripped + instExtended

# Set song title.
title = random.choice(cnfs).generate_title()

#set tempo
tempo = random.randint(80,140)

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
print("CONNIE presents \"{}\".".format(title))
print("CONNIE is now playing {} variations on {} unique bars at a tempo of {}BPM.".format(variations, uniqueBars,tempo))
print("CONNIE is employing the following instruments for this composition: " + ', '.join(map(str, instSet)))
# Do the following four times:
# Iterate through each bar
# Generate a variation on that bar
# Play that variation four times
for i in range(variations):
	for b in bars:
		v = b.getVariant()
		for i in range(repeats):
			v.play(p, tempo)
