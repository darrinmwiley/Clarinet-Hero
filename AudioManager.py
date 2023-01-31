import array
import math
import music21
import pyaudio
import pygame
import pygame_gui
import tensorflow as tf
import threading
import time
import wave

from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

from PlayConfig import PlayConfig
from Prediction import Prediction
from pygame import Surface

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
        # TODO analyze current frames before clearing here
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

    def to_audio_bytes(self, score, bpm):
        seconds_per_beat = 60 / bpm
        output_bytes=bytearray(b'')
        time_signature_numerator = 4
        time_signature_denominator = 4
        for component in score.recurse():
            if isinstance(component, music21.meter.TimeSignature):
                time_signature_numerator = component.numerator
                time_signature_denominator = component.denominator
            if isinstance(component, music21.stream.Measure):
                for sub in component.recurse():
                    if isinstance(sub, music21.note.Note):
                        duration_in_seconds = (time_signature_denominator / 4) * sub.quarterLength * seconds_per_beat
                        num_samples = int(44100 * duration_in_seconds)
                        samples = [math.sin(2 * math.pi * k * sub.pitch.frequency / 44100) for k in range(0, num_samples)]
                        output_bytes.extend(array.array('f', samples).tobytes())
                    if isinstance(sub, music21.note.Rest):
                        duration_in_seconds = (time_signature_denominator / 4) * sub.quarterLength * seconds_per_beat
                        num_samples = int(44100 * duration_in_seconds)
                        samples = [0 for k in range(0, num_samples)]
                        output_bytes.extend(array.array('f', samples).tobytes())
        return bytes(output_bytes)

    def play(self, bytes):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        stream.write(bytes)
