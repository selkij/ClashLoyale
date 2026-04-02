from enum import IntEnum


class GameState(IntEnum):
    MENU = 1
    DECK_SELECTION = 2
    GAME = 3
    PAUSED = 4
    END_GAME = 5
    EXIT = 6


class StateManager:
    def __init__(self, initial_state: GameState, screens: dict | None = None):
        self.state = initial_state
        self.screens = screens or {}

    def run_screen(self):
        return self.screens[self.state].run()

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
