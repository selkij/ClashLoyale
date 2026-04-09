import pygame

import constant
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

        self.font_small = pygame.font.Font(constant.FONTS_PATH / "YouBlockhead.ttf", 24)
        self.font_medium = pygame.font.Font(constant.FONTS_PATH / "YouBlockhead.ttf", 36)
        self.font_large = pygame.font.Font(constant.FONTS_PATH / "YouBlockhead.ttf", 76)

        self.components = []

        log.logger.send("Initialized UI")

    def add_component(self, component):
        self.components.append(component)

    def clear_components(self):
        self.components = []

    def render(self):
        self.screen.fill(constant.BACKGROUND_COLOR)
        for component in self.components:
            component.render()

    def handle_events(self, events):
        for event in events:
            for component in self.components:
                component.handle_event(event)

    def on_state_change(self):
        self.clear_components()  # Clear the existing components
        self.screen.fill(constant.BACKGROUND_COLOR)  # Clears the screen
