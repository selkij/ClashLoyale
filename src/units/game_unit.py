from __future__ import annotations

import pygame

from constant import SPRITES_PATH
from core import asset
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
        self.effect = definition.get("effect") if isinstance(definition.get("effect"), dict) else {}
        self.tower_damage = self._optional_number(definition.get("tower_damage"))

        self.state = "idle"
        self.target: GameUnit | None = None
        self.attack_timer = 0
        self.hit_flash = 0
        self.stun_timer = 0
        self.rage_timer = 0
        self.charge_timer = 0
        self.inferno_target_id = None
        self.inferno_damage = self.damage
        self.elixir_timer = 0
        self.spawn_damage_done = False
        self.death_spawned = False
        self.dead = False

        self.animations = self._load_animations()
        self.tower_image = self._load_tower_image()
        self.current_animation = "stand"
        self.size = self._get_draw_size()

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
        self.stun_timer = max(0, self.stun_timer - dt)
        self.rage_timer = max(0, self.rage_timer - dt)

        if self.hp <= 0:
            self.dead = True
            self.state = "dead"
            return

        self._update_passive_effects(dt, manager)
        self._apply_spawn_effects(manager)

        if self.stun_timer > 0:
            self.state = "idle"
            self._update_animation(dt)
            return

        self.target = manager.find_target_for(self)
        if self.target is None:
            self.state = "move" if self.speed > 0 else "idle"
            self._update_charge(dt, moving=False)
            self.inferno_target_id = None
            self.inferno_damage = self.damage
            self._move_to_default_goal(dt, manager)
            self._update_animation(dt)
            return

        if self.distance_to(self.target) <= manager.to_pixels(self.range):
            self.state = "attack"
            self._attack_target(manager)
        else:
            self.state = "move" if self.speed > 0 else "idle"
            self._try_jump(manager)
            self._update_charge(dt, moving=True)
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

        if self.rage_timer > 0:
            pygame.draw.circle(screen, (205, 40, 210), rect.center, self.size // 2 + 4, 3)
        if self.stun_timer > 0:
            pygame.draw.circle(screen, (255, 230, 80), rect.center, self.size // 2 + 8, 3)
        if self.hit_flash > 0:
            pygame.draw.circle(screen, (255, 255, 255), rect.center, self.size // 2, 3)

        self._draw_hp_bar(screen, rect)

    def take_damage(self, amount: float) -> None:
        self.hp -= amount
        self.hit_flash = 0.12
        if self.hp <= 0:
            self.dead = True
            self.state = "dead"

    def heal(self, amount: float) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    def apply_stun(self, duration: float) -> None:
        self.stun_timer = max(self.stun_timer, duration)
        self.attack_timer = max(self.attack_timer, duration)
        self.charge_timer = 0
        self.inferno_damage = self.damage

    def apply_rage(self, duration: float) -> None:
        self.rage_timer = max(self.rage_timer, duration)

    def distance_to(self, other: "GameUnit") -> float:
        return self.position.distance_to(other.position)

    def _attack_target(self, manager) -> None:
        if self.target is None or self.attack_timer > 0:
            return

        damage = self._get_attack_damage()
        if self.effect.get("damage_mutliplicator"):
            damage = self._get_inferno_damage()

        if self.target_mode == "zone" or self.self_destruct:
            radius = manager.to_pixels(max(self.radius, 1))
            manager.damage_area(
                self.target.position,
                radius,
                damage,
                self.camp,
                tower_damage=self._tower_damage_or(damage),
                source_unit=self
            )
            recoil = self._number(self.effect.get("hit_recoil", self.effect.get("recoil", 0)), 0)
            if recoil:
                manager.apply_recoil_area(self.target.position, radius, recoil, self.camp)
        else:
            self.target.take_damage(self._tower_damage_or(damage) if self.target.is_building else damage)
            if self.effect.get("hit_recoil"):
                manager.apply_recoil(self.target, self.position, self._number(self.effect.get("hit_recoil"), 0))

        if self.effect.get("stunt") and self.target is not None and not self.target.dead:
            self.target.apply_stun(self._number(self.effect.get("stunt"), 0))

        if self.self_destruct:
            self.dead = True
            self.state = "dead"
            return

        self.charge_timer = 0
        self.attack_timer = max(0.05, self._get_attack_delay())

    def _move_toward(self, destination: pygame.Vector2, dt: float, manager) -> None:
        if self.speed <= 0:
            return

        direction = destination - self.position
        if direction.length_squared() == 0:
            return

        distance = self._get_speed() * manager.tile_size * dt
        if direction.length() <= distance:
            self.position = pygame.Vector2(destination)
        else:
            self.position += direction.normalize() * distance

    def _move_to_default_goal(self, dt: float, manager) -> None:
        if self.speed <= 0:
            return

        self._move_toward(manager.default_goal_for(self), dt, manager)

    def _update_passive_effects(self, dt: float, manager) -> None:
        if self.effect.get("add_elexir"):
            self.elixir_timer += dt
            interval = self._number(self.effect.get("freq_add_elexir"), 1)
            while self.elixir_timer >= interval:
                self.elixir_timer -= interval
                manager.add_elixir(self.camp, self._number(self.effect.get("add_elexir"), 0))

    def _apply_spawn_effects(self, manager) -> None:
        if self.spawn_damage_done:
            return
        self.spawn_damage_done = True

        if self.name != "mega_knight":
            return

        radius = manager.to_pixels(self._number(self.effect.get("zone_jump_radius"), self.radius or 1))
        damage = self._number(self.effect.get("damage_jump"), self.damage)
        manager.damage_area(self.position, radius, damage, self.camp, tower_damage=self.tower_damage)

    def _try_jump(self, manager) -> None:
        if self.name != "mega_knight" or self.target is None or self.attack_timer > 0:
            return

        distance = self.distance_to(self.target)
        min_distance = manager.to_pixels(self._number(self.effect.get("jump_min"), 0))
        max_distance = manager.to_pixels(self._number(self.effect.get("jump_max"), 0))
        if not min_distance <= distance <= max_distance:
            return

        direction = self.target.position - self.position
        if direction.length_squared() > 0:
            self.position = self.target.position - direction.normalize() * manager.to_pixels(self.range)

        radius = manager.to_pixels(self._number(self.effect.get("zone_jump_radius"), 1))
        damage = self._number(self.effect.get("damage_jump"), self.damage)
        manager.damage_area(self.target.position, radius, damage, self.camp, tower_damage=self.tower_damage)
        self.attack_timer = max(0.2, self._get_attack_delay())

    def _update_charge(self, dt: float, moving: bool) -> None:
        if not self.effect.get("charging_timer"):
            return

        if moving:
            self.charge_timer += dt
        else:
            self.charge_timer = 0

    def _get_speed(self) -> float:
        speed = self.speed
        if self.rage_timer > 0:
            speed *= 1.35
        if self.effect.get("charging_timer") and self.charge_timer >= self._number(self.effect.get("charging_timer"), 0):
            speed = max(speed, self._number(self.effect.get("charching_speed"), speed))
        return speed

    def _get_attack_delay(self) -> float:
        delay = self.attack_frequency
        if self.rage_timer > 0:
            delay /= 1.35
        return delay

    def _get_attack_damage(self) -> float:
        if self.effect.get("charging_timer") and self.charge_timer >= self._number(self.effect.get("charging_timer"), 0):
            return self._number(self.effect.get("charching_damage"), self.damage)
        return self.damage

    def _tower_damage_or(self, damage: float) -> float:
        if self.effect.get("charging_timer") and self.charge_timer >= self._number(self.effect.get("charging_timer"), 0):
            charge_tower_damage = self._optional_number(self.effect.get("charching_tower_damage"))
            if charge_tower_damage is not None:
                return charge_tower_damage
        return self.tower_damage if self.tower_damage is not None else damage

    def _get_inferno_damage(self) -> float:
        if self.target is None:
            return self.damage

        if self.inferno_target_id != self.target.id:
            self.inferno_target_id = self.target.id
            self.inferno_damage = self.damage
        else:
            limit = self._number(self.effect.get("limite_damage"), self.damage)
            multiplier = self._number(self.effect.get("damage_mutliplicator"), 1)
            self.inferno_damage = min(limit, self.inferno_damage * multiplier)

        return self.inferno_damage

    def _load_animations(self) -> dict[str, Animation]:
        if "tower" in self.name:
            return {}

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

    def _load_tower_image(self) -> pygame.Surface | None:
        if "tower" not in self.name:
            return None

        sprite_name = "blue tower.png" if self.camp == "blue" else "red tower.png"
        return asset.get_image(SPRITES_PATH / sprite_name).convert_alpha()

    def _current_image(self) -> pygame.Surface | None:
        if self.tower_image is not None:
            return self.tower_image

        animation = self.animations.get(self.current_animation) or self.animations.get("stand")
        if animation is None:
            return None
        return animation.get_image()

    def _get_draw_size(self) -> int:
        if "king_tower" == self.name:
            return 96
        if "tower" in self.name:
            return 86
        if self.unit_type == "infra":
            return 68
        return 54

    def _update_animation(self, dt: float) -> None:
        if self.state == "attack" and "hit" in self.animations:
            self.current_animation = "hit"
        elif self.effect.get("charging_timer") and self.charge_timer >= self._number(self.effect.get("charging_timer"), 0) and "charge" in self.animations:
            self.current_animation = "charge"
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

    @staticmethod
    def _optional_number(value) -> float | None:
        if value == "None" or value is None:
            return None
        return float(value)
