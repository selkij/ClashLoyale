from typing import Callable

import pygame


class ButtonWidget:
    def __init__(self, modules: dict, pos: tuple, image: pygame.Surface, action: Callable[[], None]):
        # Module definitions
        self.screen = modules["ui"].screen
        self.input = modules["input"]

        self.pos = pos
        self.button_image = image
        self.action = action

        self.button_image_size = image.get_size()
        self.button_image = pygame.transform.scale(self.button_image,
                                                   (self.button_image_size[0], self.button_image_size[1]))

        self.button_rect = pygame.Rect(self.pos[0],
                                       self.pos[1],
                                       self.button_image_size[0],
                                       self.button_image_size[1])

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.action()

    def render(self):
        self.screen.blit(self.button_image, (self.pos[0], self.pos[1]))
