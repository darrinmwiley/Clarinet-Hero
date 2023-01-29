import pygame
from EventListener import EventListener

class EventManager:

    def __init__(self):
        self.subscriptions = dict()
        self.listeners = []

    def add_subscriber(self, subscriber: EventListener, eventType):
        if eventType not in self.subscriptions:
            self.subscriptions[eventType] = []
        self.subscriptions[eventType].append(subscriber)

    def add_listener(self, listener: EventListener):
        self.listeners.append(listener)

    def update(self):
        for event in pygame.event.get():
            for listener in self.listeners:
                listener.process_events(event)
            if event.type in self.subscriptions:
                for subscriber in self.subscriptions[event.type]:
                    subscriber.process_events(event)
