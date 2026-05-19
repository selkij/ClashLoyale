import pygame

from constant import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITES_PATH
from core import asset
from levels.scene import Scene
from managers.unit_manager import UnitManager


class TestScreen(Scene):
    background_path = None

    def __init__(self, modules: dict):
        super().__init__(modules)
        self.clock = pygame.time.Clock()
        self.arena = None
        self.arena_rect = None
        self.unit_manager = None

    def start(self):
        super().start()

        arena = asset.get_image(SPRITES_PATH / "arena.png").convert_alpha()
        arena_ratio = SCREEN_HEIGHT / arena.get_height()
        arena_size = (int(arena.get_width() * arena_ratio), SCREEN_HEIGHT)
        self.arena = pygame.transform.scale(arena, arena_size)
        self.arena_rect = self.arena.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.unit_manager = UnitManager(self.arena_rect)
        self.unit_manager.spawn_test_map()

    def run(self):
        super().run()

        dt = self.clock.tick(60) / 1000

        self.ui.screen.blit(self.arena, self.arena_rect)
        self._draw_test_map_guides()

        self.unit_manager.update(dt)
        self.unit_manager.draw(self.ui.screen)

        self._draw_debug_text()

    def _draw_test_map_guides(self):
        river_y = self.arena_rect.centery
        bridge_width = 74
        bridge_height = 28
        bridge_color = (177, 132, 77)

        pygame.draw.line(
            self.ui.screen,
            (65, 135, 190),
            (self.arena_rect.left + 18, river_y),
            (self.arena_rect.right - 18, river_y),
            6
        )

        for x in (self.arena_rect.centerx - 95, self.arena_rect.centerx + 95):
            bridge = pygame.Rect(0, 0, bridge_width, bridge_height)
            bridge.center = (x, river_y)
            pygame.draw.rect(self.ui.screen, bridge_color, bridge, border_radius=5)
            pygame.draw.rect(self.ui.screen, (70, 48, 33), bridge, width=2, border_radius=5)

    def _draw_debug_text(self):
        text = self.ui.font_small.render(
            f"test_map - units: {len(self.unit_manager.units)}",
            True,
            (245, 245, 245)
        )
        shadow = self.ui.font_small.render(
            f"test_map - units: {len(self.unit_manager.units)}",
            True,
            (20, 20, 20)
        )
        pos = (self.arena_rect.left + 18, self.arena_rect.top + 18)
        self.ui.screen.blit(shadow, (pos[0] + 2, pos[1] + 2))
        self.ui.screen.blit(text, pos)
