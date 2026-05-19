import logging
import os

import pygame
from pygame.event import Event

from constant import DEFINITIONS_PATH
from core.input import Input
from core.sound import Sound
from core.state import StateManager, GameState
from core.ui import UI
from levels.arena import Arena
from levels.choose_deck_screen import ChooseDeckScreen
from levels.main_menu import MainMenu
from levels.test_screen import TestScreen
from units.unit import Unit
from utils import log


class Game:
    def __init__(self):
        self.running = True
        self.modules = {
            "state": StateManager(GameState.STARTING),
            "ui": UI(),
            "input": Input(),
            "sound": Sound(16)  # 16 Channels
        }

        self.main_menu = MainMenu(self.modules)
        self.modules["state"].screens[GameState.MENU] = self.main_menu

        self.choose_deck_screen = ChooseDeckScreen(self.modules)
        self.modules["state"].screens[GameState.DECK_SELECTION] = self.choose_deck_screen

        self.test_screen = TestScreen(self.modules)
        self.modules["state"].screens[GameState.TEST] = self.test_screen

        self.arena_scene = Arena(self.modules)
        self.modules["state"].screens[GameState.GAME] = self.arena_scene

        self.registered_units = []

        for definition in os.listdir(DEFINITIONS_PATH):
            if definition.endswith(".json"):
                unit = Unit(definition)
                self.registered_units.append(unit)

        log.logger.send(f"Registered {len(self.registered_units)} units", logging.DEBUG)

        # Add screens here with state definitions
        # Example: self.test_menu = TestMenu(self.modules, ...)
        #          self.state.screens[GameState.TEST] = self.test_menu
        # For more info on how to create a scene, see test_screen.py

        log.logger.send("Initialized game")
        self.modules["state"].set_state(GameState.TEST)

    def tick(self, events: list[Event], dt):
        self.modules["input"].process(events)
        self.modules["ui"].handle_events(events)
        self.modules["state"].run_screen()
        self.modules["ui"].render()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False


