from TextButton import TextButton
from AudioHandler import AudioHandler
from Component import Component
from TimeSignature import TimeSignature
import time
import pygame
from Note import Note
from pygame import Surface
import math
import array
import pyaudio
import threading

class PlayerScreen(Component):
    def __init__(self, serviceRegistry):
        super().__init__()
        self.audioHandler = serviceRegistry["AUDIOHANDLER"]
        self.audioHandler.startRecording()
        self.screenHandler = serviceRegistry["SCREENHANDLER"]
        self.startButton = TextButton("START")
        self.add(self.startButton, (100,100), (500, 100))
        self.startButton.onClicked = lambda: self.start()
        self.started = False

    def preRender(self, notes, timeSignature, bpm):
        pixelsPerSecond = 200
        HEIGHT = 700
        TOP_NOTE = 89
        BOTTOM_NOTE = 50
        numNotes = TOP_NOTE - BOTTOM_NOTE + 1
        verticalPixelsPerNote = HEIGHT / numNotes
        secondsPerBeat = 60 / bpm
        totalBeats = 0
        totalDuration = 0
        for note in notes:
            totalDuration += (timeSignature.beatNote / note.lengthDenominator) * secondsPerBeat
        display = Surface((int(pixelsPerSecond * totalDuration + 701), 700))
        totalDuration = 0
        for note in notes:
            startX = int(totalDuration * pixelsPerSecond)
            distanceFromBottom = (note.pitch - BOTTOM_NOTE + 1) * verticalPixelsPerNote
            startY = int(700 - (verticalPixelsPerNote * (note.pitch - BOTTOM_NOTE)))
            durationInSeconds = (timeSignature.beatNote / note.lengthDenominator)#this seems wrong
            wid = int(durationInSeconds * pixelsPerSecond)
            totalDuration += durationInSeconds * secondsPerBeat
            pygame.draw.rect(display, (255,255,255), pygame.Rect(startX, startY, wid, verticalPixelsPerNote))
        self.display = display
        self.audioBytes = self.toAudioBytes(notes, timeSignature, bpm)

    def start(self):
        notes = self.fromFile("cmajor.txt")
        self.preRender(notes, TimeSignature(4,4), 60)
        self.notes = self.fromFile("cmajor.txt")
        self.startTime = time.time()
        self.started = True;
        t = threading.Thread(target = lambda: self.play(self.audioBytes))
        t.daemon = True
        t.start()

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
            notes.append(Note(denom, (octave + 1) * 12 + note))
        return notes

    def play(self, bytes):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        stream.write(bytes)


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

    def processEvent(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.startButton.isHovered():
                self.startButton.onClicked()

    def render(self, display):
        pixelsPerSecond = 200
        if self.started:
            elapsedSeconds = time.time() - self.startTime
            startX = elapsedSeconds * pixelsPerSecond
            #print(elapsedSeconds, self.display.get_width(), startX,0,min(startX + 700, self.display.get_width()), 700)
            sub = self.display.subsurface(pygame.Rect(startX,0,min(700, self.display.get_width() - startX), 700))
            display.blit(sub, (0,0))
        else:
            self.startButton.render(display)

    def midiToNote(self, midi):
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        if midi == -1: return "no note detected"
        if midi == 21: return "A0"
        if midi == 22: return "A#0"
        if midi == 23: return "B0"
        distanceFromC1 = midi - 24
        octave = 1 + distanceFromC1 // 12
        note = notes[distanceFromC1 % 12]
        return note+str(octave)
