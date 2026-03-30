import logging
import pygame

import constant
from utils import log


class UI:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen_width = constant.SCREEN_WIDTH
        self.screen_height = constant.SCREEN_HEIGHT

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        self.caption = "Clash Loyale"
        pygame.display.set_caption(self.caption)

        self.icon = pygame.image.load(constant.SPRITES_PATH / "game_icon.png")
        pygame.display.set_icon(self.icon)

        log.logger.send("Initialized UI and pygame", logging.DEBUG)

    def draw_background(self):
        self.screen.fill(constant.BACKGROUND_COLOR)
