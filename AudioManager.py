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

#todo - split prediction from audio IO

class AudioManager:
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.audio_stream = self.pyaudio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK);
        self.stored_predictions: list[Prediction] = []

    def start_recording(self):
        self.frames: list[bytes] = []
        self.samples = bytearray(b'')
        t = threading.Thread(target = self.audio_capture)
        t.daemon = True
        self.recording = True
        t.start()
        t2 = threading.Thread(target = self.store_predictions)
        t2.daemon = True
        t2.start()

    def stop_recording(self):
        self.recording = False
        #maybe analyze current frames before clearing here
        self.frames.clear()

    def audio_capture(self):
        while self.recording:
            data: bytes = self.audio_stream.read(CHUNK)
            self.frames.append(data)
            self.samples.extend(data)

    def get_most_recent_snippet(self, length_ms):
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
