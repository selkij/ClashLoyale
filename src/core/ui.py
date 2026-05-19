import pygame

import constant
from core import asset
from core.scaling import auto_scaling
from utils import log


class UI:
    def __init__(self):
        self.screen_width = constant.SCREEN_WIDTH
        self.screen_height = constant.SCREEN_HEIGHT
        self.window_width, self.window_height, self.scale_ratio = auto_scaling()

        self.display = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.screen = pygame.Surface((self.screen_width, self.screen_height)).convert()

        self.caption = "Clash Loyale"
        pygame.display.set_caption(self.caption)

        self.icon = asset.get_image(constant.SPRITES_PATH / "game_icon.png")
        pygame.display.set_icon(self.icon)

        self.font_small = asset.get_font(constant.FONTS_PATH / "YouBlockhead.ttf", 24)
        self.font_medium = asset.get_font(constant.FONTS_PATH / "YouBlockhead.ttf", 36)
        self.font_large = asset.get_font(constant.FONTS_PATH / "YouBlockhead.ttf", 76)

        self.components = []

        log.logger.send("Initialized UI")

    def get_mouse_pos(self) -> tuple[int, int]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return int(mouse_x / self.scale_ratio), int(mouse_y / self.scale_ratio)

    def present(self):
        if self.scale_ratio == 1:
            self.display.blit(self.screen, (0, 0))
        else:
            scaled_screen = pygame.transform.smoothscale(
                self.screen,
                (self.window_width, self.window_height)
            )
            self.display.blit(scaled_screen, (0, 0))

        pygame.display.flip()

    def add_component(self, component):
        self.components.append(component)

    def clear_components(self):
        self.components = []

    def render(self):
        # self.screen.fill(constant.BACKGROUND_COLOR)
        for component in self.components:
            component.render()

    def handle_events(self, events):
        for event in events:
            for component in self.components:
                component.handle_event(event)

    def on_state_change(self):
        self.clear_components()  # Clear the existing components
