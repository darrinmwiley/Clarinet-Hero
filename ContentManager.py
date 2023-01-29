import pygame
import music21

class ContentManager:

    def __init__(self):
        self.logo = pygame.image.load('resources/clarinethero.png')
        self.logo = pygame.transform.scale(self.logo, (750, 425))

    def from_file(self, file_path):
        return music21.converter.parse(file_path)
