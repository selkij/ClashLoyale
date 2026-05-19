from __future__ import annotations

import pygame

from constant import SPRITES_PATH
from core.animation import Animation


SPRITE_NAME_OVERRIDES = {
    "hogrider": "hog_rider",
    "sapeur": "wall_breaker",
    "x_bow": "X-bow",
    "infernal_tower": "inferno_tower",
    "elexir_pump": "elixir_pump",
}


class GameUnit:
    def __init__(self, unit_id: int, definition: dict, camp: str, position: tuple[float, float]):
        self.id = unit_id
        self.definition = definition
        self.name = definition["name"]
        self.camp = camp
        self.position = pygame.Vector2(position)
        self.max_hp = self._number(definition.get("pv"), 1)
        self.hp = self.max_hp
        self.damage = self._number(definition.get("damage"), 0)
        self.attack_frequency = self._number(definition.get("freq_atk"), 1)
        self.speed = self._number(definition.get("speed"), 0)
        self.unit_type = definition.get("type", "unit")
        self.range = self._number(definition.get("range"), 1)
        self.radius = self._number(definition.get("radius"), 0)
        self.target_mode = definition.get("target", "unique")
        self.self_destruct = bool(definition.get("self_destruct", 0))

        self.state = "idle"
        self.target: GameUnit | None = None
        self.attack_timer = 0
        self.hit_flash = 0
        self.dead = False

        self.animations = self._load_animations()
        self.current_animation = "stand"
        self.size = 54 if self.unit_type != "infra" else 68

    @property
    def is_building(self) -> bool:
        return self.unit_type == "infra" or "tower" in self.name

    @property
    def center(self) -> pygame.Vector2:
        return self.position

    def update(self, dt: float, manager) -> None:
        if self.dead:
            return

        self.hit_flash = max(0, self.hit_flash - dt)
        self.attack_timer = max(0, self.attack_timer - dt)

        if self.hp <= 0:
            self.dead = True
            self.state = "dead"
            return

        if self.self_destruct:
            self._explode(manager)
            return

        self.target = manager.find_target_for(self)
        if self.target is None:
            self.state = "move" if self.speed > 0 else "idle"
            self._move_to_default_goal(dt, manager)
            self._update_animation(dt)
            return

        if self.distance_to(self.target) <= manager.to_pixels(self.range):
            self.state = "attack"
            self._attack_target()
        else:
            self.state = "move" if self.speed > 0 else "idle"
            self._move_toward(self.target.center, dt, manager)

        self._update_animation(dt)

    def draw(self, screen: pygame.Surface) -> None:
        image = self._current_image()
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = self.position

        if image is None:
            color = (40, 120, 255) if self.camp == "blue" else (235, 70, 55)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (20, 20, 20), rect, width=2, border_radius=8)
        else:
            scaled = pygame.transform.smoothscale(image, rect.size)
            screen.blit(scaled, rect)

        if self.hit_flash > 0:
            pygame.draw.circle(screen, (255, 255, 255), rect.center, self.size // 2, 3)

        self._draw_hp_bar(screen, rect)

    def take_damage(self, amount: float) -> None:
        self.hp -= amount
        self.hit_flash = 0.12
        if self.hp <= 0:
            self.dead = True
            self.state = "dead"

    def distance_to(self, other: "GameUnit") -> float:
        return self.position.distance_to(other.position)

    def _attack_target(self) -> None:
        if self.target is None or self.attack_timer > 0:
            return

        self.target.take_damage(self.damage)
        self.attack_timer = max(0.05, self.attack_frequency)

    def _explode(self, manager) -> None:
        manager.damage_area(self.position, manager.to_pixels(max(self.radius, 1)), self.damage, self.camp)
        self.dead = True
        self.state = "dead"

    def _move_toward(self, destination: pygame.Vector2, dt: float, manager) -> None:
        if self.speed <= 0:
            return

        direction = destination - self.position
        if direction.length_squared() == 0:
            return

        distance = self.speed * manager.tile_size * dt
        if direction.length() <= distance:
            self.position = pygame.Vector2(destination)
        else:
            self.position += direction.normalize() * distance

    def _move_to_default_goal(self, dt: float, manager) -> None:
        if self.speed <= 0:
            return

        self._move_toward(manager.default_goal_for(self), dt, manager)

    def _load_animations(self) -> dict[str, Animation]:
        sprite_camp = "blue_unit_png" if self.camp == "blue" else "red_unit_png"
        sprite_name = SPRITE_NAME_OVERRIDES.get(self.name, self.name)
        base_path = SPRITES_PATH / sprite_camp

        animations = {}
        for animation_name in ("stand", "run", "hit", "charge"):
            try:
                frames = Animation.load_animation(base_path, sprite_name, animation_name)
                animations[animation_name] = Animation(frames, frame_duration=0.12, loop=True)
            except FileNotFoundError:
                pass

        return animations

    def _current_image(self) -> pygame.Surface | None:
        animation = self.animations.get(self.current_animation) or self.animations.get("stand")
        if animation is None:
            return None
        return animation.get_image()

    def _update_animation(self, dt: float) -> None:
        if self.state == "attack" and "hit" in self.animations:
            self.current_animation = "hit"
        elif self.state == "move" and "run" in self.animations:
            self.current_animation = "run"
        elif "stand" in self.animations:
            self.current_animation = "stand"

        animation = self.animations.get(self.current_animation)
        if animation is not None:
            animation.update(dt)

    def _draw_hp_bar(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        if self.max_hp <= 1:
            return

        ratio = max(0, self.hp / self.max_hp)
        bg_rect = pygame.Rect(rect.left, rect.top - 9, rect.width, 5)
        hp_rect = pygame.Rect(bg_rect.left, bg_rect.top, int(bg_rect.width * ratio), bg_rect.height)
        color = (55, 145, 255) if self.camp == "blue" else (240, 80, 65)

        pygame.draw.rect(screen, (25, 25, 25), bg_rect)
        pygame.draw.rect(screen, color, hp_rect)

    @staticmethod
    def _number(value, fallback: float) -> float:
        if value == "None" or value is None:
            return fallback
        return float(value)
