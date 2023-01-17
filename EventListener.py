from typing import Protocol
import pygame

class EventListener(Protocol):
    def processEvent(self, event: pygame.event) -> None: ...
