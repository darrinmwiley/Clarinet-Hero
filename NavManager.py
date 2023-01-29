import pygame
import pygame_gui
from MainMenuScreenV2 import MainMenuScreenV2
from AudioManager import AudioManager
from PredictionManager import PredictionManager

class NavManager:

    def __init__(self, services):
        self.screens = dict()
        self.screens["MAINMENU"] = MainMenuScreenV2(services)
        self.set_current_screen("MAINMENU")
        services["EVENTMANAGER"].add_listener(self)

    def set_current_screen(self, name):
        self.current_screen = self.screens[name]

    def process_events(self, event):
        self.current_screen.process_events(event)

    def update(self, time_delta):
        self.current_screen.update(time_delta)

    def render(self, display):
        self.current_screen.render(display)
