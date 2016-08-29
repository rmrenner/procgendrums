import mido
import time
import random
import NameGen

class Instrument():
    def __init__(self, name, midiVal, probabilities):
        self.name = name
        self.msg = mido.Message('note_on', note=midiVal,velocity=127,channel=9)
        self.probabilities = probabilities
        self.patterns = []
        self.playing = True
        self.current_pattern = 0
        self.pattern_count = 8
        for i in range(self.pattern_count):
            print("{} pattern {}".format(self.name, i))
            self.patterns.append(Pattern(self))

    def __str__(self):
        return self.name

    def play(self, port, position):
        p = self.patterns[self.current_pattern]
        if(p.pattern[position]):
            port.send(self.msg)

    def incrementPlaycount(self):
        p = self.patterns[self.current_pattern]
        p.incrementPlaycount()
        if(not p.playing):
            self.current_pattern += 1
        if(self.current_pattern >= len(self.patterns)):
            self.playing = False

class Pattern():
    def __init__(self, instrument):
        self.instrument = instrument
        self.playing = True
        self.playcount = 0
        self.maxplaycount = 8
        ready = False
        while(not ready):
            s = ""
            self.pattern = []
            for i in self.instrument.probabilities:
                x = random.randint(1,8)
                ready = ready or (x <= i)
                if (x <= i):
                    s += "X"
                    self.pattern.append(True)
                else:
                    s += "0"
                    self.pattern.append(False)
            print(s)

    def incrementPlaycount(self):
        self.playcount += 1
        if(self.playcount >= self.maxplaycount):
            self.playing = False

class Composition:
    def __init__(self, midiPort, instruments):
        self.midiPort = midiPort
        self.kick = Instrument("kick", 0x24, [8,0,0,1,4,0,1,1,6,0,3,1,4,1,2,1])
        self.instruments = instruments
        self.tempo = random.randint(110,140)
        self.sixteenth = 60.0 / (self.tempo * 4)
        self.playing = True
        self.barNumber = 1


    # Randomly varies the tempo of the composition
    def varyTempo(self):
        i = random.randint(1,8)
        if(i == 1):
            self.tempo -= 5.0
        elif(i == 8):
            self.tempo += 5.0
        self.tempo = min(max(80, self.tempo),140)
        self.sixteenth = 60.0 / (self.tempo * 4)

    def play(self):

        # Grab a random subset of instruments.
        inst = [self.kick] + random.sample(self.instruments, random.randint(0, len(self.instruments)))
        #inst = random.sample(self.instruments, 4)

        print("BAR{}: {} at {}BPM".format(self.barNumber, ', '.join(map(str, inst)),self.tempo))

        # Go each step in our patterns:
        for i in range(4):
            for j in range(16):
                for x in inst:
                    x.play(self.midiPort, j)
                time.sleep(self.sixteenth)

        self.barNumber += 1
        for x in inst:
            # Increment the playcount of each pattern played
            x.incrementPlaycount()
            # Clear out instruments that have run their course
            if(not x.playing):
                #self.instruments.remove(x)
                self.playing = False
        # if we've run out of instruments, we're done
        if(len(self.instruments)==0):
            self.playing = False

def instrumentSetup():
    # Create instruments
    # Define instrument midi values
#    kick = Instrument("kick", 0x24, [8,0,0,1,4,0,1,1,6,0,3,1,4,1,2,1])
    snare = Instrument("snare", 0x26, [0,0,0,0,7,0,0,1,1,3,0,0,7,0,1,1])
    lotom = Instrument("lo tom", 0x2b, [0,1,2,2,0,1,2,2,0,2,1,3,2,1,5,1])
    hitom = Instrument("hi tom", 0x32, [0,0,2,1,0,0,0,3,2,4,1,3,0,0,1,0])
    clhat = Instrument("cl hat", 0x2a, [4,2,7,3,4,3,7,3,4,2,6,2,4,2,5,2])
    ophat = Instrument("op hat", 0x2e, [0,0,1,0,0,0,1,1,0,1,3,0,0,0,1,0])
    clap = Instrument("clap", 0x27, [0,0,0,1,4,0,1,0,2,0,1,1,5,0,1,0])
    claves = Instrument("claves", 0x4b, [1,2,3,2,3,3,3,2,3,1,1,5,2,1,2,1])
    agogo = Instrument("agogo", 0x43, [1,0,3,0,1,2,2,2,1,1,2,1,1,1,3,1])
    crash = Instrument("crash", 0x31, [1,2,1,3,1,1,3,1,1,2,1,2,1,1,3,2])

    # Create instrument set
    # Instrument sets:
    instExtended = [lotom, hitom, clap, claves, agogo, crash]
    instStripped = [snare, clhat, ophat]
    instSet = instStripped + instExtended
    return instSet


# Initialize midi port
p = mido.open_output(u'mio')

# Create composition object
c = Composition(p, instrumentSetup())
songTitle = NameGen.generate()
print("********************")
print("NOW PLAYING:")
print("{}".format(songTitle))
print("********************")

while(c.playing):
  c.play()
  #c.varyTempo()
