from pathlib import Path
import pygame

from constant import SPRITES_PATH
from core import asset
from core.animation import Animation

from levels.scene import Scene
from levels.widgets.image_widget import ImageWidget
from levels.widgets.text_widget import TextWidget


BASE_UNIT_PATH = SPRITES_PATH / "blue_unit_png"

class TestScreen(Scene):

    def __init__(self, modules: dict):
        super().__init__(modules)

    def start(self):
        super().start()

        components = [
            TextWidget(
                self.modules,
                "TextWidget",
                self.ui.font_small,
                (50, 50)
            ),

            ImageWidget(
                self.modules,
                (100, 100),
                asset.get_image(SPRITES_PATH / "arena.png"),
                id="ImageWidgetTest"
            )
        ]
        for component in components:
            self.ui.add_component(component)

        run_frames = []


        run_frames = Animation.load_animation(
             BASE_UNIT_PATH,
            "zappy",
            "charge"
        )

        self.run_animation = Animation(
            run_frames,
            frame_duration=0.12,
            loop=True
        )
       

        self.knight_widget = ImageWidget(
            self.modules,
            (400, 300),
            self.run_animation.get_image(),
            id="KnightAnim"
        )

        self.ui.add_component(self.knight_widget)

        self.clock = pygame.time.Clock()

    def run(self):
        super().run()


        dt = self.clock.tick(60) / 1000

        self.run_animation.update(dt)

        self.knight_widget.image = self.run_animation.get_image()
    
    


