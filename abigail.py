# ABIGAIL is the first draft of a generative music script
# for the Korg Volca Beats.

# ABIGAIL generates 32 nonrepeating bars of randomized music at the BPM specified by tempo
# Each bar contains 16 16th notes.
# The probability that an instrument i will sound at a given step t
# is based on how often i is triggered at time t in the eight factory preset patterns
# of the Volca Beats.

# For example, each demo pattern begins with a kick, so there's a 100% chance
# that each bar begins with a kick.
# Likewise, snares are very likely to trigger on the 2nd and 4th beats of every bar.

# The probabilities derived from these patterns are far from representative of
# any particular genre, and dramatically different effects can be achieved just
# by manipulating these frequencies arbitrarily or by using a different set
# of source patterns.

import mido
import time
import random

kick = 0x24
snare = 0x26
lotom = 0x2b
hitom = 0x32
clhat = 0x2a
ophat = 0x2e
clap = 0x27
claves = 0x4b
agogo = 0x43
crash = 0x31

#set tempo
tempo = 120
hexnote = 60.0 / (tempo * 4)

#set instrument trigger probabilities
pkick = [8,0,0,1,4,0,1,1,6,0,3,1,4,1,2,1]
psnare = [0,0,0,0,7,0,0,1,1,3,0,0,7,0,1,1]
plotom = [0,1,2,2,0,1,2,2,0,2,1,3,2,1,5,1]
phitom = [0,0,2,1,0,0,0,3,2,4,1,3,0,0,1,0]
pclhat = [4,2,7,3,4,3,7,3,4,2,6,2,4,2,5,2]
pophat = [0,0,1,0,0,0,1,1,0,1,3,0,0,0,1,0]
pclap = [0,0,0,1,4,0,1,0,2,0,1,1,5,0,1,0]
pclaves = [1,2,3,2,3,3,3,2,3,1,1,5,2,1,2,1]
pagogo = [1,0,3,0,1,2,2,2,1,1,2,1,1,1,3,1]
pcrash = [1,2,1,3,1,1,3,1,1,2,1,2,1,1,3,2]

pinst=[pkick,psnare,plotom,phitom,pclhat,pophat,pclap,pclaves,pagogo,pcrash]
#pinst=[pkick,psnare,pclhat,pophat]


mkick = mido.Message('note_on', note=kick,velocity=127,channel=9)
msnare = mido.Message('note_on', note=snare,velocity=127,channel=9)
mlotom = mido.Message('note_on', note=lotom,velocity=127,channel=9)
mhitom = mido.Message('note_on', note=hitom,velocity=127,channel=9)
mclhat = mido.Message('note_on', note=clhat,velocity=127,channel=9)
mophat = mido.Message('note_on', note=ophat,velocity=127,channel=9)
mclap = mido.Message('note_on', note=clap,velocity=127,channel=9)
mclaves = mido.Message('note_on', note=claves,velocity=127,channel=9)
magogo = mido.Message('note_on', note=agogo,velocity=127,channel=9)
mcrash = mido.Message('note_on', note=crash,velocity=127,channel=9)

inst = [mkick, msnare, mlotom, mhitom, mclhat, mophat, mclap,mclaves,magogo,mcrash]
#inst = [mkick, msnare, mclhat, mophat]

port = mido.open_output(u'mio')
#Generate a bar of 16th notes 32 times
for i in range(1,32):
	#go through each of the 16th notes
	for j in range(16):
		#go through each instrument and decide if it plays
		for k in range(len(inst)):
			x = random.randint(1,8)
			if (x <= pinst[k][j]):
				port.send(inst[k])
		time.sleep(hexnote)