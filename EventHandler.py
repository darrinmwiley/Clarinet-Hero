import pygame
from EventListener import EventListener

class EventHandler:

    def __init__(self):
        self.subscriptionMapping = dict()

    def addSubscriber(self, subscriber: EventListener, eventType):
        if eventType not in self.subscriptionMapping:
            self.subscriptionMapping[eventType] = []
        self.subscriptionMapping[eventType].append(subscriber)

    def update(self):
        for event in pygame.event.get():
            if event.type in self.subscriptionMapping:
                for subscriber in self.subscriptionMapping[event.type]:
                    subscriber.processEvent(event)
