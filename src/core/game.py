import pygame
from pygame.event import Event

from core.input import Input
from core.sound import Sound
from core.state import StateManager, GameState
from core.ui import UI
from levels.main_menu import MainMenu
from levels.game_screen import GameScreen
from utils import log


class Game:
    def __init__(self):
        self.running = True
        self.state = StateManager(GameState.GAME)

        self.ui = UI()
        self.input = Input(self.state)
        self.sound = Sound()

        self.main_menu = MainMenu(self.ui.screen, self.state)
        self.state.screens[GameState.MENU] = self.main_menu
        self.game_screen = GameScreen(self.ui.screen, self.state)
        self.state.screens[GameState.GAME] = self.game_screen

        self.sound.play_music("combat.mp3")
        self.sound.set_volume(1) # LA VALEUR DOIT ETRE ENTRE 0 ET 1

        # Add screens here with state definitions
        # Example: self.test_menu = TestMenu(self.ui.screen, self.state)
        #          self.state.screens[GameState.TEST] = self.test_menu
        # For more info on how to create a scene, see test_screen.py
        log.logger.send("Initialized game")

    def tick(self, events: list[Event], dt):
        self.ui.render()
        self.state.run_screen()
        self.input.process(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
