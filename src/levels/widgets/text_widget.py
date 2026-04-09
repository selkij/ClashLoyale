import pygame.font


class TextWidget:
    def __init__(self, modules: dict, text: str, font: pygame.font.Font, pos: tuple, color: tuple = (255, 255, 255)):
        # Module definitions
        self.screen = modules["ui"].screen
        self.font = font

        self.text = text
        self.pos = pos
        self.color = color

    def render(self):
        surface = self.font.render(self.text, True, self.color)
        self.screen.blit(surface, self.pos)

    def handle_event(self, events):
        pass
