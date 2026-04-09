from core.state import StateManager


class TestScreen:
    def __init__(self, modules: dict, state_manager: StateManager):
        # Module definitions
        self.ui = modules["ui"]
        self.state_manager = state_manager

    def run(self):
        self.ui.screen.fill('red')
