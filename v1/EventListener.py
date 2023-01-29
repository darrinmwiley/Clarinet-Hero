from typing import Protocol
import pygame

class EventListener(Protocol):
    def process_events(self, event: pygame.event) -> None: ...
