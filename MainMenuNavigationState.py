from Buttons import RectangularButton
import pygame

class MainMenuNavigationState:

    def __init__(self, serviceRegistry):
        self.navigationManager = serviceRegistry["NAVIGATIONMANAGER"]
        startButton = RectangularButton(100,585,500,100,"start")
        startButton.onClicked = lambda:print("start button clicked")
        tuningButton = RectangularButton(100,475,500,100,"tuning")
        tuningButton.onClicked = lambda:self.navigationManager.navigate("TUNING")
        self.buttons = [ startButton, tuningButton]
        self.image = pygame.image.load('clarinethero.png')
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
