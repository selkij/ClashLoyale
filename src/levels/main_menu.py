import pygame

import constant
from core import asset
from core.state import GameState
from levels.scene import Scene
from levels.widgets.button_widget import ButtonWidget


class MainMenu(Scene):
    background_path = constant.GUI_PATH / "loading_cl.png"

    def __init__(self, modules: dict):
        super().__init__(modules)  # Initializes the scene

        self.state_manager = modules["state"]
        self.input = modules["input"]
        self.sound = modules["sound"]

    def start(self):
        super().start()

        play_sprite = asset.get_image(constant.WIDGETS_PATH / 'play_icon.png').convert_alpha()
        play_sprite = pygame.transform.scale(play_sprite, (96, 96))
        test_sprite = self.ui.font_medium.render("TEST MAP", True, constant.TEXT_COLOR)

        components = [
            ButtonWidget(
                self.modules,
                (35, constant.SCREEN_HEIGHT - 120),
                play_sprite,
                lambda _: self.state_manager.set_state(GameState.DECK_SELECTION)
            ),
            ButtonWidget(
                self.modules,
                (145, constant.SCREEN_HEIGHT - 93),
                test_sprite,
                lambda _: self.state_manager.set_state(GameState.TEST)
            )
        ]

        for component in components:
            self.ui.add_component(component)

        self.sound.play_sound("deck.mp3", 2500, True)

    def run(self):
        super().run()
