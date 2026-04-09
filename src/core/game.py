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
        self.modules = {
            "state": StateManager(GameState.MENU),
            "ui": UI(),
            "input": Input(),
            "sound": Sound()
        }

        self.main_menu = MainMenu(self.modules)
        self.modules["state"].screens[GameState.MENU] = self.main_menu

        # Add screens here with state definitions
        # Example: self.test_menu = TestMenu(self.modules, ...)
        #          self.state.screens[GameState.TEST] = self.test_menu
        # For more info on how to create a scene, see test_screen.py
        log.logger.send("Initialized game")

    def tick(self, events: list[Event], dt):
        self.modules["input"].process(events)
        self.modules["ui"].handle_events(events)
        self.modules["state"].run_screen()
        self.modules["ui"].render()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
