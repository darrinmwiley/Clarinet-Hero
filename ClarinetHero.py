import pygame
from NavigationManager import NavigationManager
from EventManager import EventManager
from AudioInputManager import AudioInputManager

class ClarinetHero:
    def __init__(self):
        pygame.init() # library module
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.display = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.eventManager = EventManager()
        self.audioInputManager = AudioInputManager()
        self.serviceRegistry = {"CLARINETHERO": self, "EVENTMANAGER": self.eventManager, "AUDIOINPUTMANAGER": self.audioInputManager}
        self.navigationManager = NavigationManager(self.serviceRegistry)
        self.eventManager.addSubscriber(self, pygame.QUIT)

    def render(self):
        self.navigationManager.render(self.display)
        pygame.display.flip()

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
