from typing import Callable

import pygame

from levels.widgets.button_widget import ButtonWidget
from levels.widgets.text_widget import TextWidget


class ButtonWithTipWidget:
    def __init__(self, modules: dict, text: str, font: pygame.font.Font, pos: tuple, image: pygame.Surface,
                 action: Callable[[], None], text_color: tuple = (255, 255, 255)):
        # Module definitions
        self.ui = modules["ui"]
        self.screen = self.ui.screen
        self.input = modules["input"]
        self.font = font

        self.pos = pos
        self.button_image = image
        self.action = action
        self.text = text
        self.text_color = text_color

        self.button = ButtonWidget(modules, pos, self.button_image, action)
        text_pos = (
            self.pos[0] + self.button_image.get_width() + 10,
            self.pos[1] - self.font.get_height() / 2 + self.button_image.get_height() / 2
        )
        self.text = TextWidget(modules, self.text, self.font, text_pos, self.text_color)

    def handle_event(self, event: pygame.event.Event):
        self.button.handle_event(event)
        self.text.handle_event(event)

    def render(self):
        self.button.render()
        self.text.render()
