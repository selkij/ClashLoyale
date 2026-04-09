import pygame

import constant
from constant import WIDGETS_PATH
from levels.widgets.ButtonWithTipWidget import ButtonWithTipWidget
from levels.widgets.centered_text_widget import CenteredTextWidget


def blank():
    pass


class MainMenu:
    def __init__(self, modules: dict):
        self.state_manager = modules["state"]
        self.input = modules["input"]
        self.ui = modules["ui"]
        self.sound = modules["sound"]

        # TODO: Centralized image loading system
        play_sprite = pygame.image.load(WIDGETS_PATH / 'play_icon.png').convert_alpha()
        play_sprite = pygame.transform.scale(play_sprite, (96, 96))

        components = [
            ButtonWithTipWidget(
                modules,
                "Play",
                self.ui.font_medium,
                (25, self.ui.screen_height - 100),
                play_sprite,
                blank
            ),

            CenteredTextWidget(
                modules,
                "Clash Loyale",
                self.ui.font_large,
                (self.ui.screen_width / 2, 30)
            )
        ]

        for component in components:
            self.ui.add_component(component)

        self.sound.play_music("deck.mp3")

    def run(self):
        self.ui.screen.fill(constant.BACKGROUND_COLOR)
