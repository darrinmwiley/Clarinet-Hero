from TextButton import TextButton
from Component import Component
import pygame

class MainMenuScreen(Component):

    def __init__(self, serviceRegistry):
        super().__init__()
        self.screenHandler = serviceRegistry["SCREENHANDLER"]
        startButton = TextButton("start")
        tuningButton = TextButton("tuning")
        self.add(startButton, (100, 585), (500, 100))
        self.add(tuningButton, (100, 475), (500, 100))
        startButton.onClicked = lambda:self.screenHandler.navigate("PLAYER")
        tuningButton.onClicked = lambda:self.screenHandler.navigate("TUNING")
        self.buttons = [ startButton, tuningButton]
        self.image = pygame.image.load('resources/clarinethero.png')
        self.image = pygame.transform.scale(self.image, (500, 384))

    def processEvent(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.isHovered():
                    button.onClicked()

    def render(self, display):
        pygame.draw.rect(display, (208,206,164), pygame.Rect(0,0,700,700))
        for button in self.buttons:
            button.render(display)
        display.blit(self.image, (100, 40))
