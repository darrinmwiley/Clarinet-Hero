import pygame
from ScreenHandler import ScreenHandler
from EventHandler import EventHandler
from AudioHandler import AudioHandler

class ClarinetHero:
    def __init__(self):
        pygame.init() # library module
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.display: pygame.Surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.eventHandler = EventHandler()
        self.audioHandler = AudioHandler()
        self.serviceRegistry = {"CLARINETHERO": self, "EVENTHANDLER": self.eventHandler, "AUDIOHANDLER": self.audioHandler}
        self.screenHandler = ScreenHandler(self.serviceRegistry)
        self.eventHandler.addSubscriber(self, pygame.QUIT)

    def render(self):
        self.screenHandler.render(self.display)
        pygame.display.flip()

    def updateGameLogic(self):
        self.eventHandler.update()

    def start(self):
        self.running = True
        while self.running:
            self.updateGameLogic()
            self.render()

    def processEvent(self, event: pygame.event):
        if event.type == pygame.QUIT:
            self.running = False

if __name__ == '__main__':
    ClarinetHero().start()
