import threading
import pygame
import pyaudio
import wave
import time
from Prediction import Prediction
import tensorflow as tf
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

class PredictionManager:
    def __init__(self, services):
        self.services = services
        self.stored_predictions: list[Prediction] = []
        t = threading.Thread(target = self.load_model)
        t.daemon = True
        t.start()

    def load_model(self):
        self.basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))

    def store_predictions(self, snippet_length_ms = 200):
        while self.services["AUDIOMANAGER"].recording:
            note_activations = self.predict(snippet_length_ms)
            snippet_end_time_ms = time.time() * 1000;
            snippet_start_time_ms = snippet_end_time_ms - snippet_length_ms
            self.stored_predictions.append(Prediction(snippet_start_time_ms, snippet_end_time_ms, note_activations))

    def predict_note_at_timestamp(self, timestamp_millis):
        L = -1
        R = len(self.stored_predictions)
        M = int((L+R) // 2)
        while R - L > 1:
            M = int((L + R) // 2)
            prediction = self.stored_predictions[M]
            if prediction.snippet_start_time_ms <= timestamp_millis:
                L = M
            else:
                R = M
        current_index = L
        note_count = dict()
        relevantFrames = 0
        while current_index >= 0 and self.stored_predictions[current_index].snippet_end_time_ms > timestamp_millis:
            prediction = self.stored_predictions[current_index]
            note_activations = self.stored_predictions[current_index].note_activations
            if len(note_activations) == 0:
                pitch = -1
                if pitch not in note_count:
                    note_count[pitch] = 0
                note_count[pitch] = note_count[pitch] + 1
            relevantFrames+=1
            for activation in note_activations:
                pitch = activation[2]
                if pitch not in note_count:
                    note_count[pitch] = 0
                note_count[pitch] = note_count[pitch] + 1
            current_index-=1
        max = 0
        note = -1
        for key, value in note_count.items():
            if value > max:
                max = value
                note = key
        if max > relevantFrames / 2:
            return note
        else:
            return -1

    def predict(self, snippet_length_ms = 200):
        if self.services["AUDIOMANAGER"].get_most_recent_snippet(snippet_length_ms):
            model_output, midi_data, note_activations = predict("sample.wav", self.basic_pitch_model, onset_threshold=.6, frame_threshold=.6, minimum_frequency=27.5, maximum_frequency=4186)
            return note_activations
        return []
