import pygame

class Component():

    def __init__(self):
        self.parent = None
        self.children = []

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getRelativePosition(self):
        return self.relativePosition

    def getAbsolutePosition(self):
        if self.parent == None:
            return self.getRelativePosition()
        (parentAbslX, parentAbslY) = self.getParent().getAbsolutePosition()
        (relX, relY) = self.getRelativePosition()
        return (parentAbslX + relX, parentAbslY + relY)

    def setRelativePosition(self, coordinates):
        self.relativePosition = coordinates

    def setSize(self, size):
        self.size = size

    def getChildren(self):
        return self.children

    def add(self, child, coordinates, size):
        child.onAddedToParent(self, coordinates, size)
        self.children.append(child)

    def onAddedToParent(self, parent, coordinates, size):
        self.setRelativePosition(coordinates)
        self.setSize(size)
        self.setParent(parent)

    def clearChildren(self):
        while len(self.children) != 0:
            self.children.pop().setParent(None)

    def getSize(self):
        return self.size

    def setSize(self, size):
        self.size = size

    def render(self, display):
        (x,y) = self.getRelativePosition()
        (wid, ht) = self.getSize()
        pygame.draw.rect(display, (208,206,164), pygame.Rect(x,y,wid,ht))
        for child in self.children:
            child.render(display)

    def isHovered(self):
        parent = self.getParent()
        if parent is not None and parent.isHovered() == False:
            return False
        return self.coordinatesInBoundsAbsl(pygame.mouse.get_pos())

    def coordinatesInBoundsAbsl(self, coordinates):
        (x,y) = coordinates
        if self.parent == None:
            return True
        (abslX, abslY) = self.getAbsolutePosition()
        (wid, ht) = self.getSize()
        print(self, abslX, abslY, wid, ht)
        return abslX <= x <= abslX + wid and abslY <= y <= abslY + ht

    def processEvent(self, event):
        pass
