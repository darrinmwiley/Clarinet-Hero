import pygame
from EventListener import EventListener

class EventHandler:

    def __init__(self):
        self.subscriptions = dict()

    def addSubscriber(self, subscriber: EventListener, eventType):
        if eventType not in self.subscriptions:
            self.subscriptions[eventType] = []
        self.subscriptions[eventType].append(subscriber)

    def update(self):
        for event in pygame.event.get():
            if event.type in self.subscriptions:
                for subscriber in self.subscriptions[event.type]:
                    subscriber.process_events(event)
