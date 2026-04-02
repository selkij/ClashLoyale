import constant

class GameScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state

    def run(self):
        self.screen.fill(constant.BACKGROUND_COLOR)
