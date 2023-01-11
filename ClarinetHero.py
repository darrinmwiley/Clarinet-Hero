import pygame
import time
from NavigationManager import NavigationManager
from EventManager import EventManager

class ClarinetHero:
    def __init__(self):
        pygame.init() # library module
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.display = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.navigationManager = NavigationManager()
        self.eventManager = EventManager()
        self.eventManager.addSubscriber(self, pygame.QUIT)

    # rendering will be done here
    def render(self):
        self.navigationManager.render(self.display)
        pygame.display.flip()

    # detection and timing will be done here
    def updateGameLogic(self):
        self.eventManager.update()

    def start(self):
        self.running = True
        while self.running:
            self.updateGameLogic()
            self.render()

    def processEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False

if __name__ == '__main__':
    ClarinetHero().start()
