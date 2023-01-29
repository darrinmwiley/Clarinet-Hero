import winsound
from collections import deque
from Note import Note
from TimeSignature import TimeSignature
import time
import math
import pyaudio
import array

class Synth:

    def play(self, notes, timeSignature, bpm):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        stream.write(self.toAudioBytes(notes, timeSignature, bpm))


    def toAudioBytes(self, notes, timeSignature, bpm):
        secondsPerBeat = 60 / bpm
        totalBeats = 0
        output_bytes=bytearray(b'')
        for note in notes:
            #note duration in seconds
            duration = (timeSignature.beatNote / note.lengthDenominator) * secondsPerBeat
            num_samples = int(44100 * duration)
            samples = [note.volume * math.sin(2 * math.pi * k * note.frequency() / 44100) for k in range(0, num_samples)]
            output_bytes.extend(array.array('f', samples).tobytes())
        return bytes(output_bytes)


    def fromFile(self, fname):
        f = open(fname, "r")
        text = f.read()
        arr = text.split(" ")
        notes = []
        for str in arr:
            split = str.split("/")
            notestr = split[0][0:-1]
            noteArray = ["c","c#","d","d#","e", "f", "f#", "g", "g#", "a", "a#", "b"]
            note = noteArray.index(notestr)
            octave = int(split[0][1])
            denom = int(split[1])
            notes.append(Note(denom, octave * 12 + note))
        return notes

synth = Synth()
notes = synth.fromFile("cmajor.txt")
timeSignature = TimeSignature(4,4)
synth.play(notes, timeSignature, 120)
time.sleep(2)
