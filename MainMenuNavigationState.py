from Buttons import RectangularButton
import pygame

class MainMenuNavigationState:
    def __init__(self, navigationManager):
        self.navigationManager = navigationManager
        self.startButton = RectangularButton(100,585,500,100,"start")
        self.tuningButton = RectangularButton(100,475,500,100,"tuning")
        self.image = pygame.image.load('clarinethero.png')
        self.image = pygame.transform.scale(self.image, (500, 384))


    def render(self, display):
        pygame.draw.rect(display, (208,206,164), pygame.Rect(0,0,700,700))
        self.startButton.render(display)
        self.tuningButton.render(display)
        display.blit(self.image, (100, 40))
