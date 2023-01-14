import threading
import pygame
import pyaudio
import wave
import time

from Prediction import Prediction

import tensorflow as tf

from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))


CHUNK = 1024 # number of samples read in at a time
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050 # sampling rate per second
# every chunk is (1/RATE)*(CHUNK) seconds (~46ms)
# due to paInt16 format, every sample is 2 bytes
SAMPLES_PER_MS = RATE/1000;

class AudioInputManager:
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.audioStream = self.pyaudio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK);
        self.storedPredictions = []

    def startRecording(self):
        self.frames = []
        self.samples = bytearray(b'')
        t = threading.Thread(target = self.audioCapture)
        t.daemon = True
        self.recording = True
        t.start()
        t2 = threading.Thread(target = self.storePredictions)
        t2.daemon = True
        t2.start()

    def stopRecording(self):
        self.recording = False
        #maybe analyze current frames before clearing here
        self.frames = []

    def audioCapture(self):
        while self.recording:
            data = self.audioStream.read(CHUNK)
            self.frames.append(data)
            self.samples.extend(data)

    def storePredictions(self):
        snippetLengthMs = 200
        while self.recording:
            noteActivations = self.predict(snippetLengthMs)
            snippetEndTimeMs = time.time() * 1000;
            snippetStartTimeMs = snippetEndTimeMs - snippetLengthMs
            self.storedPredictions.append(Prediction(snippetStartTimeMs, snippetEndTimeMs, noteActivations))

    def predictNoteAtTimestamp(self, timestampMillis):
        L = -1
        R = len(self.storedPredictions)
        M = int((L+R) // 2)
        while R - L > 1:
            M = int((L + R) // 2)
            prediction = self.storedPredictions[M]
            #print(prediction.snippetStartTimeMs, prediction.snippetEndTimeMs, timestampMillis)
            if prediction.snippetStartTimeMs <= timestampMillis:
                #print("L = M")
                L = M
            else:
                #print("R = M")
                R = M
        currentIndex = L
        noteCount = dict()
        #print(self.storedPredictions[currentIndex].snippetStartTimeMs, self.storedPredictions[currentIndex].snippetEndTimeMs, timestampMillis, "(final)")
        while currentIndex >= 0 and self.storedPredictions[currentIndex].snippetEndTimeMs > timestampMillis:
            prediction = self.storedPredictions[currentIndex]
            #print(timestampMillis, prediction.snippetStartTimeMs, prediction.snippetEndTimeMs, prediction.noteActivations)
            noteActivations = self.storedPredictions[currentIndex].noteActivations
            #if len(noteActivations) == 0:
            #    pitch = -1
            #    if pitch not in noteCount:
            #        noteCount[pitch] = 0
            #    noteCount[pitch] = noteCount[pitch] + 1
            for activation in noteActivations:
                pitch = activation[2]
                if pitch not in noteCount:
                    noteCount[pitch] = 0
                noteCount[pitch] = noteCount[pitch] + 1
            currentIndex-=1
        max = 0
        note = -1
        for key, value in noteCount.items():
            if value > max:
                max = value
                note = key
        return note

    def getMostRecentSnippet(self, length_ms):
        num_samples = int(length_ms * SAMPLES_PER_MS)
        if num_samples * 2 < len(self.samples):
            wf = wave.open("sample.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.pyaudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(self.samples[-num_samples*2:])
            wf.close()
            return True
        return False

    #200
    def predict(self, snippetLengthMs):
        if self.getMostRecentSnippet(snippetLengthMs):
            model_output, midi_data, note_activations = predict("sample.wav", basic_pitch_model, onset_threshold=.5, frame_threshold=.5, minimum_frequency=27.5, maximum_frequency=4186)
            return note_activations
        return []
