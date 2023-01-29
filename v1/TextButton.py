import pygame
from Button import Button

class TextButton(Button):
    def __init__(self,text):
        self.text = text

    def renderHover(self, display):
        color = (220,220,220)
        (tlx, tly) = self.getRelativePosition()
        (wid, ht) = self.getSize()
        pygame.draw.rect(display, color, pygame.Rect(tlx, tly, wid, ht))
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render(self.text, False, (0,0,0))
        text_x = tlx + (wid - text_surface.get_width()) / 2
        text_y = tly + (ht - text_surface.get_height()) / 2
        display.blit(text_surface, (text_x, text_y))

    def render(self, display):
        if self.isHovered():
            self.renderHover(display)
        else:
            color = (200,200,200)
            (tlx, tly) = self.getRelativePosition()
            (wid, ht) = self.getSize()
            pygame.draw.rect(display, color, pygame.Rect(tlx, tly, wid, ht))
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = font.render(self.text, False, (0,0,0))
            text_x = tlx + (wid - text_surface.get_width()) / 2
            text_y = tly + (ht - text_surface.get_height()) / 2
            display.blit(text_surface, (text_x, text_y))
