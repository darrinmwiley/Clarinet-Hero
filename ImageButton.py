import pygame
from Button import Button

class ImageButton(Button):
    def __init__(self, imagePath):
        self.image = pygame.image.load(imagePath)

    def onAddedToParent(self, parent, coordinates, size):
        super().onAddedToParent(parent, coordinates, size)
        (wid, ht) = self.getSize()
        self.image = pygame.transform.scale(self.image, (self.getSize()))

    def renderHover(self, display):
        #todo alternate hover while rendering
        (tlx, tly) = self.getRelativePosition()
        (wid, ht) = self.getSize()
        pygame.draw.rect(display, (220,220,220), pygame.Rect(tlx, tly, wid, ht))
        display.blit(self.image, (tlx, tly))

    def render(self, display):
        if self.isHovered():
            self.renderHover(display)
        else:
            (tlx, tly) = self.getRelativePosition()
            (wid, ht) = self.getSize()
            pygame.draw.rect(display, (200,200,200), pygame.Rect(tlx, tly, wid, ht))
            display.blit(self.image, (tlx, tly))
