# import pygame package
import threading
import pygame
import pyaudio
import wave
import time

import tensorflow as tf

from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))

audio_window_seconds = 3;

CHUNK = 1024 # number of samples read in at a time
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050 # sampling rate per second
# every chunk is (1/RATE)*(CHUNK) seconds (~46ms)
# due to paInt16 format, every sample is 2 bytes
SAMPLES_PER_MS = RATE/1000;

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK);
begin_time_millis = time.time() * 1000;

frames = []
samples = bytearray(b'')

def audioCapture():
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        samples.extend(data)

def getMostRecentSnippet(length_ms):
    num_samples = int(length_ms * SAMPLES_PER_MS)
    if num_samples * 2 < len(samples):
        wf = wave.open("sample.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(samples[-num_samples*2:])
        wf.close()
        return True
    return False

if __name__ == '__main__':
    # initializing imported module
    pygame.init()

    t = threading.Thread(target = audioCapture)
    t.daemon = True
    t.start()
    # displaying a window of height
    # 500 and width 400
    window = pygame.display.set_mode((400, 500))

    # creating a bool value which checks
    # if game is running
    running = True
    last_update_millis = begin_time_millis
    # keep game running till running is true
    while running:
        if getMostRecentSnippet(200):
            model_output, midi_data, note_activations = predict("sample.wav", basic_pitch_model, onset_threshold=.8, frame_threshold=.7, minimum_frequency=27.5, maximum_frequency=4186)
            pitches = []
            pygame.draw.rect(window, (0,0,0), pygame.Rect(0,0,400,500))
            for tuple in note_activations:
                start_time_s = tuple[0]
                end_time_s = tuple[1]
                pitch = tuple[2]
                velocity = tuple[3]
                #velocity = tuple[3];
                print(pitch, velocity)
                pygame.draw.rect(window, (255,255,255), pygame.Rect(pitch*4,0,4,100))

        #print("ms since last update", time.time() * 1000 - last_update_millis)
        last_update_millis = time.time() * 1000;
        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():

            # if event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

        # set background color to our window

        # Update our window
        pygame.display.flip()
