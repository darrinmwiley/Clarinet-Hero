import pygame

class RectangularButton:
    def __init__(self, tlx, tly, wid, ht, text):
        self.tlx = tlx
        self.tly = tly
        self.wid = wid
        self.ht = ht
        self.text = text

    def coordinates_in_bounds(self, x, y):
        return x >= self.tlx and x <= self.tlx + self.wid and y >= self.tly and y <= self.tly + self.ht

    def renderHover(self, display):
        color = (220,220,220)
        pygame.draw.rect(display, color, pygame.Rect(self.tlx, self.tly, self.wid, self.ht))
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render(self.text, False, (0,0,0))
        text_x = self.tlx + (self.wid - text_surface.get_width()) / 2
        text_y = self.tly + (self.ht - text_surface.get_height()) / 2
        display.blit(text_surface, (text_x, text_y))

    def isHovered(self):
        (x, y) = pygame.mouse.get_pos()
        return self.coordinates_in_bounds(x,y)

    def render(self, display):
        if self.isHovered():
            self.renderHover(display)
        else:
            color = (200,200,200)
            pygame.draw.rect(display, color, pygame.Rect(self.tlx, self.tly, self.wid, self.ht))
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = font.render(self.text, False, (0,0,0))
            text_x = self.tlx + (self.wid - text_surface.get_width()) / 2
            text_y = self.tly + (self.ht - text_surface.get_height()) / 2
            display.blit(text_surface, (text_x, text_y))
