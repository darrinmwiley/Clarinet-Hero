import pygame
import music21

class ContentManager:

    def __init__(self):
        self.logo = pygame.image.load('resources/clarinethero.png')
        self.logo = pygame.transform.scale(self.logo, (750, 425))

    def from_file(self, file_path):
        return music21.converter.parse(file_path)

    def get_total_num_beats(self, score):
         for component in score.recurse():
             if isinstance(component, music21.note.Note):
                print(component, component.beams)

cm = ContentManager()
score = cm.from_file("fmajor.musicxml")
beats = cm.get_total_num_beats(score)
print(beats)
