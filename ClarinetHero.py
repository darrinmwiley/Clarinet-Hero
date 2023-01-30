import pygame
import pygame_gui
from AudioManager import AudioManager
from ContentManager import ContentManager
from EventManager import EventManager
from NavManager import NavManager
from PredictionManager import PredictionManager

class ClarinetHero:
    def __init__(self):
        pygame.init() # library module
        self.display = pygame.display.set_mode((800,600))
        self.services = dict()
        self.services["CONTENTMANAGER"] = ContentManager()
        self.services["EVENTMANAGER"] = EventManager()
        self.services["NAVMANAGER"] = NavManager(self.services)
        self.services["AUDIOMANAGER"] = AudioManager()
        self.services["PREDICTIONMANAGER"] = PredictionManager(self.services)
        self.services["EVENTMANAGER"].add_subscriber(self, pygame.QUIT)

    def update(self, time_delta):
        self.services["EVENTMANAGER"].update()
        self.services["NAVMANAGER"].update(time_delta)

    def render(self, display):
        pygame.draw.rect(display, (208,206,164), pygame.Rect(0,0,800,600))
        self.services["NAVMANAGER"].render(display)
        pygame.display.update()

    def start(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            time_delta = clock.tick(60)/1000.0
            self.update(time_delta)
            self.render(self.display)

    def process_events(self, event: pygame.event):
        if event.type == pygame.QUIT:
            self.running = False

if __name__ == '__main__':
    ClarinetHero().start()
