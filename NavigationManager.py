from Buttons import RectangularButton
from MainMenuNavigationState import MainMenuNavigationState

class NavigationManager:
    #todo: support multiple open navs rendering in order
    #todo: pipe events into navigation states
    def __init__(self):
        self.mainMenuNavigationState = MainMenuNavigationState(self)

    def render(self, display):
        self.mainMenuNavigationState.render(display)
