import pygame
import pygame_gui

class MainMenuScreenV2:

    def __init__(self, services):
        self.ui = pygame_gui.UIManager((800,600))
        settings_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((25,475),(350, 100)), text = "Settings", manager = self.ui)
        start_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((425,475),(350, 100)), text = "Start", manager = self.ui)
        self.logo = pygame.image.load('resources/clarinethero.png')
        self.logo = pygame.transform.scale(self.logo, (750, 425))
        self.onButtonPress = dict()
        self.onButtonPress[start_button] = lambda:  print("start clicked")
        self.onButtonPress[settings_button] = lambda: print("settings clicked")

    def process_events(self,event):
        self.ui.process_events(event)
        if(event.type == pygame_gui.UI_BUTTON_PRESSED):
            if event.ui_element in self.onButtonPress:
                self.onButtonPress[event.ui_element]()


    def update(self, time_delta):
        self.ui.update(time_delta)

    def render(self, display):
        self.ui.draw_ui(display)
        display.blit(self.logo, (25, 25))
