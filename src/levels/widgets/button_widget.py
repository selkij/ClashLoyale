from typing import Any, Callable

import pygame

from utils import tracked_surface


class ButtonWidget:
    def __init__(self, modules: dict, pos: tuple, image: pygame.Surface | tracked_surface.TrackedSurface,
                 action: Callable[[Any], None], id: str | None = None):
        # Module definitions
        self.ui = modules["ui"]
        self.screen = self.ui.screen
        self.input = modules["input"]

        self.pos = pos

        if type(image) == tracked_surface.TrackedSurface:
            self.button_image = image.surface
        else:
            self.button_image = image

        self.action = action
        self.id = id

        self.action = lambda: action(self)  # Passes the object to the action

        self.button_image_size = self.button_image.get_size()
        # self.button_image = pygame.transform.scale(self.button_image,
        #                                           (self.button_image_size[0], self.button_image_size[1]))

        self.button_rect = pygame.Rect(self.pos[0],
                                       self.pos[1],
                                       self.button_image_size[0],
                                       self.button_image_size[1])

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(self.ui.get_mouse_pos()):
                self.action()

    def render(self):
        self.screen.blit(self.button_image, (self.pos[0], self.pos[1]))
