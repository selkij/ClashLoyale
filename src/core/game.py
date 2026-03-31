import pygame
from pygame.event import Event

from core.input import Input
from core.sound import Sound
from core.ui import UI
from utils import log


class Game:
    def __init__(self):
        self.ui = UI()
        self.input = Input()
        self.sound = Sound()
        self.running = True

        log.logger.send("Initialized game")

    def tick(self, events: list[Event], dt):
        self.ui.render()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

