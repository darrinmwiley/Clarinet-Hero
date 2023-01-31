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

    def __init__(self, services):
        self.services = services
        self.load(PlayConfig()
                    .newBuilder()
                    .set_score(services["CONTENTMANAGER"].load_musicxml("fmajor.musicxml"))
                    .set_bpm(60)
                    .build())
        self.started = False

    def load(self, config):
        self.config = config
        self.audio_bytes = self.services["AUDIOMANAGER"].to_audio_bytes(config.score, config.bpm)

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
        start_x = int((time_offset - elapsed_seconds) * pixels_per_second)
        duration_in_seconds = (time_signature_denominator / 4) * note.quarterLength * seconds_per_beat
        wid = int(duration_in_seconds * pixels_per_second)
        if (start_x + wid) > 0 and start_x < remaining_display_width:
            diatonic_pitch = note.pitch.diatonicNoteNum
            distanceFromBottom = (diatonic_pitch - bottom_note_diatonic + 1) * vertical_pixels_per_note
            startY = int(display_height - (vertical_pixels_per_note * (diatonic_pitch - bottom_note_diatonic)) - vertical_pixels_per_note / 2)
            endX = min(start_x + wid, remaining_display_width)
            actualstart_x = max(0, start_x)
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
            if start_x < 0:
                note_surface = note_surface.subsurface(pygame.Rect(int(-start_x),0,int(wid + start_x), int(vertical_pixels_per_note * 2)))
            display.blit(note_surface, (actualstart_x + self.treble_clef_width,startY))

    def start(self):
        self.start_time = time.time()
        self.started = True;
        t = threading.Thread(target = lambda: self.services["AUDIOMANAGER"].play(self.audio_bytes))
        t.daemon = True
        t.start()

    def process_events(self,event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            self.start()

    def update(self, time_delta):
        pass

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
