import pygame

import constant
from core import asset
from core.state import GameState
from levels.scene import Scene
from levels.widgets.button_widget import ButtonWidget


class EndGameScreen(Scene):
    def __init__(self, modules):
        super().__init__(modules)
        self.state_manager = modules["state"]
        self.sound = modules["sound"]

    def start(self):
        super().start()
        self.sound.clear_sounds()

        button_surface = asset.get_image(constant.WIDGETS_PATH / "button_base.png").convert_alpha()
        button_surface = pygame.transform.scale(button_surface, (260, 88))
        menu_surface = self.ui.font_small.render("MENU", True, constant.TEXT_COLOR)
        button_surface.blit(menu_surface, menu_surface.get_rect(center=(130, 44)))

        self.ui.add_component(ButtonWidget(
            self.modules,
            (constant.SCREEN_WIDTH / 2 - 130, constant.SCREEN_HEIGHT / 2 + 130),
            button_surface,
            lambda _: self.state_manager.set_state(GameState.MENU)
        ))

    def run(self):
        super().run()

        winner = self.state_manager.winner
        if winner == "egalite":
            title = "EGALITE"
            color = constant.TEXT_COLOR
        else:
            title = f"VICTOIRE {str(winner).upper()}"
            color = constant.BLUE_COLOR if winner == "bleu" else constant.RED_COLOR

        title_surface = self.ui.font_large.render(title, True, color)
        title_rect = title_surface.get_rect(center=(constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2 - 80))
        self.ui.screen.blit(title_surface, title_rect)
