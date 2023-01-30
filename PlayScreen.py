import pygame
import pygame_gui
import music21
from pygame import Surface
import time
import math
import array
import pyaudio
import threading
from PlayConfig import PlayConfig

class PlayScreen:

    def __init__(self):
        self.load(PlayConfig()
                    .newBuilder()
                    .set_score(self.from_file("fmajor.musicxml"))
                    .set_bpm(60)
                    .build())
        self.started = False

    def load(self, config):
        self.config = config
        self.audioBytes = self.toAudioBytes(config.score, config.bpm)

    def draw_staff(self, display):
        display_width = display.get_width()
        display_height = display.get_height()
        bottom_note_diatonic = self.config.bottom_note_diatonic
        top_note_diatonic = self.config.top_note_diatonic
        number_of_notes = top_note_diatonic - bottom_note_diatonic + 1
        vertical_pixels_per_note = display_height / number_of_notes
        treble_clef_bottom_note_diatonic = 30
        treble_clef_top_note_diatonic = 38
        for i in range(treble_clef_bottom_note_diatonic, treble_clef_top_note_diatonic + 1,2):
            line_y = int(display_height - (vertical_pixels_per_note * (i - bottom_note_diatonic + 1)) + vertical_pixels_per_note / 2)
            pygame.draw.line(display, (0,0,0), (0, line_y), (display_width, line_y))
        bottom_bar_y = int(display_height - (vertical_pixels_per_note * (30 - bottom_note_diatonic + 1)) + vertical_pixels_per_note / 2)
        top_bar_y = int(display_height - (vertical_pixels_per_note * (38 - bottom_note_diatonic + 1)) + vertical_pixels_per_note / 2)
        staff_height = bottom_bar_y - top_bar_y
        treble_clef_height = int(staff_height / .689) + 1
        treble_clef_y = int(top_bar_y - treble_clef_height * .087)
        treble_clef_width = int(treble_clef_height * .367)
        treble_clef_image = pygame.image.load('resources/trebleclef.png')
        treble_clef_image = pygame.transform.scale(treble_clef_image, (treble_clef_width, treble_clef_height))
        display.blit(treble_clef_image, (0,treble_clef_y))
        self.treble_clef_width = treble_clef_width


    def draw_note(self, note, display, elapsed_seconds, time_signature_denominator):
        remaining_display_width = display.get_width() - self.treble_clef_width
        display_height = display.get_height()
        bottom_note_diatonic = self.config.bottom_note_diatonic
        top_note_diatonic = self.config.top_note_diatonic
        bpm = self.config.bpm
        number_of_notes = top_note_diatonic - bottom_note_diatonic + 1
        vertical_pixels_per_note = display_height / number_of_notes
        seconds_per_beat = 60/bpm
        seconds_to_display = self.config.seconds_to_display
        pixels_per_second = remaining_display_width / seconds_to_display


        beat_offset = note.activeSite.offset + note.offset
        time_offset = seconds_per_beat * beat_offset
        startX = int((time_offset - elapsed_seconds) * pixels_per_second)
        durationInSeconds = (time_signature_denominator / 4) * note.quarterLength * seconds_per_beat
        wid = int(durationInSeconds * pixels_per_second)

        if (startX + wid) > 0 and startX < remaining_display_width:
            diatonic_pitch = note.pitch.diatonicNoteNum
            distanceFromBottom = (diatonic_pitch - bottom_note_diatonic + 1) * vertical_pixels_per_note
            startY = int(display_height - (vertical_pixels_per_note * (diatonic_pitch - bottom_note_diatonic)) - vertical_pixels_per_note / 2)
            endX = min(startX + wid, remaining_display_width)
            actualStartX = max(0, startX)
            #idea: draw note to its own surface and then take the subsurface that is still on the screen
            note_surface = Surface((wid, vertical_pixels_per_note * 2))
            pygame.draw.rect(note_surface, (220,220,220), pygame.Rect((0,0),(wid, vertical_pixels_per_note * 2)))
            pygame.draw.circle(note_surface, (20,20,20), (int(vertical_pixels_per_note), int(vertical_pixels_per_note)), int(vertical_pixels_per_note))
            pygame.draw.rect(note_surface, (20,20,20), pygame.Rect((int(vertical_pixels_per_note), 0), (int(wid - vertical_pixels_per_note * 2), int(vertical_pixels_per_note * 2))))
            pygame.draw.circle(note_surface, (20,20,20), (int(wid - vertical_pixels_per_note), int(vertical_pixels_per_note)), int(vertical_pixels_per_note))
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = font.render(note.pitch.nameWithOctave, False, (220, 220, 220))
            text_x = (wid - text_surface.get_width()) / 2
            text_y = (vertical_pixels_per_note * 2 - text_surface.get_height()) / 2
            note_surface.blit(text_surface, (text_x, text_y))
            if startX < 0:
                note_surface = note_surface.subsurface(pygame.Rect(int(-startX),0,int(wid + startX), int(vertical_pixels_per_note * 2)))
            display.blit(note_surface, (actualStartX + self.treble_clef_width,startY))

    def start(self):
        self.score = self.from_file("fmajor.musicxml")
        self.start_time = time.time()
        self.started = True;
        t = threading.Thread(target = lambda: self.play(self.audioBytes))
        t.daemon = True
        t.start()

    def from_file(self, file_path):
        return music21.converter.parse(file_path)

    def process_events(self,event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            self.start()

    def update(self, time_delta):
        pass

    def toAudioBytes(self, score, bpm):
        secondsPerBeat = 60 / bpm
        totalBeats = 0
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
                        durationInSeconds = (time_signature_denominator / 4) * sub.quarterLength * secondsPerBeat
                        num_samples = int(44100 * durationInSeconds)
                        samples = [math.sin(2 * math.pi * k * sub.pitch.frequency / 44100) for k in range(0, num_samples)]
                        output_bytes.extend(array.array('f', samples).tobytes())
                    if isinstance(sub, music21.note.Rest):
                        durationInSeconds = (time_signature_denominator / 4) * sub.quarterLength * secondsPerBeat
                        num_samples = int(44100 * durationInSeconds)
                        samples = [0 for k in range(0, num_samples)]
                        output_bytes.extend(array.array('f', samples).tobytes())
        return bytes(output_bytes)

    def play(self, bytes):
        print("playing")
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        stream.write(bytes)

    def render(self, display):
        pygame.draw.rect(display, (220, 220, 220), pygame.Rect(0,0,800,600))
        self.draw_staff(display)
        if self.started:
            time_signature_denominator = 4
            elapsed_seconds = time.time() - self.start_time
            for component in self.config.score.recurse():
                if isinstance(component, music21.stream.Measure):
                    for sub in component.recurse():
                        if isinstance(sub, music21.meter.TimeSignature):
                            time_signature_denominator = sub.denominator
                        if isinstance(sub, music21.note.Note):
                            self.draw_note(sub, display, elapsed_seconds, time_signature_denominator)
