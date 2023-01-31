import pygame
import music21

class ContentManager:

    def __init__(self):
        self.logo = pygame.image.load('resources/clarinethero.png')
        self.logo = pygame.transform.scale(self.logo, (750, 425))

    def load_musicxml(self, file_path):
        return music21.converter.parse(file_path)

    def get_total_num_beats(self, score):
         for component in score.recurse():
             if isinstance(component, music21.note.Note):
                print(component, component.beams)
