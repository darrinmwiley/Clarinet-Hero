from Buttons import RectangularButton
from AudioInputManager import AudioInputManager
import time
import pygame

class TuningNavigationState:
    def __init__(self, serviceRegistry):
        #todo: have service injection manager
        self.audioInputManager = serviceRegistry["AUDIOINPUTMANAGER"]
        self.audioInputManager.startRecording()
        self.navigationManager = serviceRegistry["NAVIGATIONMANAGER"]
        backToMainMenu = RectangularButton(100,475,500,100,"back to main menu")
        backToMainMenu.onClicked = lambda:self.navigationManager.navigate("MAIN_MENU")
        self.buttons = [backToMainMenu]

    def processEvent(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.isHovered():
                    button.onClicked()

    def render(self, display):
        #TODO offboard this to a thread
        note = self.audioInputManager.predictNoteAtTimestamp(time.time() * 1000 - 200)
        pygame.draw.rect(display, (208,206,164), pygame.Rect(0,0,700,700))
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render(self.midiToNote(note), False, (0,0,0))
        display.blit(text_surface, (300,300))
        for button in self.buttons:
            button.render(display)

    def midiToNote(self, midi):
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        if midi == -1: return "no note detected"
        if midi == 21: return "A0"
        if midi == 22: return "A#0"
        if midi == 23: return "B0"
        distanceFromC1 = midi - 24
        octave = 1 + distanceFromC1 // 12
        note = notes[distanceFromC1 % 12]
        return note+str(octave)
