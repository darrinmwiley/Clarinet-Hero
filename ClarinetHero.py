import pygame
import time

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

# rendering will be done here
def render():
    pygame.display.flip()

# detection and timing will be done here
def update_game_logic():
    pass

# game_tick: main loop of the game.
def game_tick():
    pygame.event.pump() # required by game library, we may use these events later
    update_game_logic()
    render()
    return True # return True to keep ticking, False to end

# init: called before the game starts ticking - do setup here
def init():
    pygame.init() # library module
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

if __name__ == '__main__':
    init()
    while game_tick(): continue
