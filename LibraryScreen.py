from TextButton import TextButton
from ImageButton import ImageButton
from Searchbar import Searchbar
from ScrollPane import ScrollPane
from ButtonList import ButtonList
from Component import Component
import pygame

class LibraryScreen(Component):

    def __init__(self, serviceRegistry):
        super().__init__()
        self.screenHandler = serviceRegistry["SCREENHANDLER"]
        self.eventHandler = serviceRegistry["EVENTHANDLER"]
        self.eventHandler.addSubscriber(self,pygame.MOUSEBUTTONUP)
        self.backButton = ImageButton("resources/backarrow.png")
        self.backButton.onClicked = lambda: self.screenHandler.navigate("MAIN_MENU")
        self.add(self.backButton, (12, 12), (50, 50))
        self.add(ImageButton("resources/upload.png"), (287, 12), (50, 50))
        self.add(Searchbar(), (74, 12), (201, 50))
        scrollPane = ScrollPane(serviceRegistry)
        self.add(scrollPane, (12, 74), (326, 614))
        self.buttonList = ButtonList()
        scrollPane.add(self.buttonList,(12, 0), (314, 614))
        for i in range(20):
            self.buttonList.addButton(TextButton("button "+str(i)))

    def processEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.backButton.isHovered():
            self.backButton.onClicked()

    #def render(self, display):
    #    pygame.draw.rect(display, (208,206,164), pygame.Rect(0,0,700,700))
    #    for component in self.components:
    #        component.render(display)
