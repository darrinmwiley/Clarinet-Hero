import pygame
from pygame import Surface
from Component import Component

class ButtonList(Component):
  def __init__(self):
      super().__init__()
      #todo add mouse wheel scroll

  def addButton(self, button):
      (wid, ht) = self.getSize()
      self.add(button, (5, len(self.getChildren()) * 55 + 5), (wid - 12, 50))
      self.setSize((wid, len(self.getChildren()) * 55 + 5))

  def getRenderedSurface(self):
      surface = Surface((self.wid,self.getHeight()))
      for button in self.buttons:
          button.render(surface)
      return surface
