import pygame
import pygame_gui
from MainMenuScreen import MainMenuScreen
from AudioManager import AudioManager
from PredictionManager import PredictionManager
from PlayScreen import PlayScreen

class NavManager:

    def __init__(self, services):
        self.screens = dict()
        self.screens["MAINMENU"] = MainMenuScreen(services)
        self.screens["PLAY"] = PlayScreen()
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
