from TextButton import TextButton
from MainMenuScreen import MainMenuScreen
from TuningScreen import TuningScreen
from LibraryScreen import LibraryScreen
from PlayerScreen import PlayerScreen
from Component import Component
import pygame

class ScreenHandler(Component):
    #todo: support multiple open navs rendering in order
    #todo: pipe events into navigation states
    def __init__(self, serviceRegistry):
        super().__init__()
        self.setRelativePosition((0,0))
        self.setSize((700,700))
        serviceRegistry["SCREENHANDLER"] = self
        self.screensByKeyword = dict()
        self.eventManager = serviceRegistry["EVENTHANDLER"]
        self.eventManager.addSubscriber(self, pygame.MOUSEBUTTONUP)
        self.screensByKeyword["MAIN_MENU"] = MainMenuScreen(serviceRegistry)
        self.screensByKeyword["TUNING"] = TuningScreen(serviceRegistry)
        #self.screensByKeyword["LIBRARY"] = LibraryScreen(serviceRegistry)
        self.screensByKeyword["PLAYER"] = PlayerScreen(serviceRegistry)
        self.navigate("MAIN_MENU")

    def navigate(self, keyword):
        self.clearChildren()
        self.add(self.screensByKeyword[keyword],(0,0),(700,700))

    def getCurrentScreen(self):
        return self.getChildren()[0]

    def processEvent(self, event):
        self.getCurrentScreen().processEvent(event)
