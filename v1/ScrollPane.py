import pygame
from Component import Component
from pygame import Surface

#todo might want to make horizontal scroll eventually

class ScrollPane(Component):
  def __init__(self, serviceRegistry):
      super().__init__()
      self.eventHandler = serviceRegistry["EVENTHANDLER"]
      self.eventHandler.addSubscriber(self, pygame.MOUSEBUTTONUP)
      self.eventHandler.addSubscriber(self, pygame.MOUSEBUTTONDOWN)
      self.eventHandler.addSubscriber(self, pygame.MOUSEMOTION)
      self.scrollTopY = 0
      self.dragging = False
      #todo add mouse wheel scroll

  def processEvent(self, event):
      (x, y) = pygame.mouse.get_pos()
      (wid, ht) = self.getSize()
      if event.type == pygame.MOUSEBUTTONDOWN:

          if self.coordinatesInScrollerBounds(x,y):
              self.dragging = True
              self.initialDragY = y
              self.initialScrollTopY = self.scrollTopY
      if event.type == pygame.MOUSEBUTTONUP:
          (x, y) = pygame.mouse.get_pos()
          if self.dragging:
              self.dragging = False
              nextScrollTopY = self.initialScrollTopY + y - self.initialDragY
              self.scrollTopY = min(ht - self.getScrollerHeight(), max(0,nextScrollTopY))
      if event.type == pygame.MOUSEMOTION:
          (x, y) = pygame.mouse.get_pos()
          if self.dragging:
              nextScrollTopY = self.initialScrollTopY + y - self.initialDragY
              self.scrollTopY = min(ht - self.getScrollerHeight(), max(0,nextScrollTopY))

  def coordinatesInScrollerBounds(self, x, y):
      (tlx, tly) = self.getRelativePosition()
      relX = x - tlx
      relY = y - tly
      return relX >= 0 and relX < 12 and relY >= self.scrollTopY and relY < self.scrollTopY + self.getScrollerHeight()

  def scrollNeeded(self):
      return self.getContent().getSize()[1] > self.getSize()[1]

  def getScrollerHeight(self):
      (wid, ht) = self.getSize()
      return ht * ht / self.getContent().getSize()[1]

  def getContent(self):
      return self.getChildren()[0]

  def render(self, display):
      (tlx, tly) = self.getRelativePosition()
      (wid, ht) = self.getSize()
      pygame.draw.rect(display, (100,100,100), pygame.Rect(tlx, tly, wid, ht))
      pygame.draw.rect(display, (20,20,20), pygame.Rect(tlx,tly + self.scrollTopY, 12, self.getScrollerHeight()))
      contentSurface = Surface(self.getContent().getSize())
      self.getContent().render(contentSurface)
      print(self, self.getContent(), contentSurface)
      if self.scrollNeeded() == False:
          display.blit(contentSurface, (tlx + 12, tly))
      else:
          startY = self.scrollTopY / ht * self.getContent().getSize()[1]
          sub = contentSurface.subsurface(pygame.Rect(0,startY, wid - 12, ht))
          display.blit(sub, (tlx + 12, tly))
