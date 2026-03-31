import pygame
from pygame.event import Event

import constant
from core.input import Input
from utils import log


class UI:
    def __init__(self):


        self.screen_width = constant.SCREEN_WIDTH
        self.screen_height = constant.SCREEN_HEIGHT

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        self.caption = "Clash Loyale"
        pygame.display.set_caption(self.caption)

        self.icon = pygame.image.load(constant.SPRITES_PATH / "game_icon.png")
        pygame.display.set_icon(self.icon)

        log.logger.send("Initialized UI and pygame")

    def render(self):
        self.screen.fill(constant.BACKGROUND_COLOR)

