import pygame
from Component import Component

class Searchbar(Component):
  def __init__(self):
      self.image = pygame.image.load("resources/search.png")

  def renderHover(self, display):
      #todo alternate hover while rendering
      (x, y) = self.getRelativePosition()
      (wid, ht) = self.getSize()
      pygame.draw.rect(display, (220,220,220), pygame.Rect(x, y, wid, ht))
      display.blit(self.image, (x, y))

  def onAddedToParent(self, parent, coordinates, size):
      super().onAddedToParent(parent, coordinates, size)
      (wid, ht) = self.getSize()
      self.image = pygame.transform.scale(self.image, (ht, ht))

  def render(self, display):
      if self.isHovered():
          self.renderHover(display)
      else:
          (x, y) = self.getRelativePosition()
          (wid, ht) = self.getSize()
          pygame.draw.rect(display, (200,200,200), pygame.Rect(x, y, wid, ht))
          display.blit(self.image, (x, y))
