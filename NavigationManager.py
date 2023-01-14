from Buttons import RectangularButton
from MainMenuNavigationState import MainMenuNavigationState
from TuningNavigationState import TuningNavigationState
import pygame

class NavigationManager:
    #todo: support multiple open navs rendering in order
    #todo: pipe events into navigation states
    def __init__(self, serviceRegistry):
        serviceRegistry["NAVIGATIONMANAGER"] = self
        self.screensByKeyword = dict()
        self.eventManager = eventManager = serviceRegistry["EVENTMANAGER"]
        self.eventManager.addSubscriber(self, pygame.MOUSEBUTTONUP)
        self.screensByKeyword["MAIN_MENU"] = MainMenuNavigationState(serviceRegistry)
        self.screensByKeyword["TUNING"] = TuningNavigationState(serviceRegistry)
        self.currentScreen = "MAIN_MENU"

    def navigate(self, keyword):
        self.currentScreen = keyword

    def getCurrentScreen(self):
        return self.screensByKeyword[self.currentScreen]

    def render(self, display):
        self.getCurrentScreen().render(display)

    def processEvent(self, event):
        self.getCurrentScreen().processEvent(event)
