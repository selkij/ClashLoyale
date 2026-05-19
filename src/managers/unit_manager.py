import json
from pathlib import Path

import pygame

from constant import DEFINITIONS_PATH
from units.game_unit import GameUnit


class UnitManager:
    def __init__(self, map_rect: pygame.Rect, tile_size: int = 44):
        self.map_rect = map_rect
        self.tile_size = tile_size
        self.units: list[GameUnit] = []
        self.next_id = 1
        self.definitions = self._load_definitions()

    def reset(self) -> None:
        self.units = []
        self.next_id = 1

    def spawn_unit(self, unit_name: str, camp: str, position: tuple[float, float]) -> GameUnit:
        definition = self.definitions[unit_name]
        unit_count = self._number(definition.get("nb_unit"), 1)
        spawned = []

        for index in range(int(unit_count)):
            offset = pygame.Vector2((index % 3) * 18, (index // 3) * 18)
            unit = GameUnit(self.next_id, definition, camp, pygame.Vector2(position) + offset)
            self.next_id += 1
            self.units.append(unit)
            spawned.append(unit)

        return spawned[0]

    def spawn_test_map(self) -> None:
        self.reset()

        left = self.map_rect.left
        top = self.map_rect.top
        width = self.map_rect.width
        height = self.map_rect.height

        self.spawn_unit("princess_tower", "blue", (left + width * 0.28, top + height * 0.82))
        self.spawn_unit("king_tower", "blue", (left + width * 0.50, top + height * 0.90))
        self.spawn_unit("princess_tower", "blue", (left + width * 0.72, top + height * 0.82))

        self.spawn_unit("princess_tower", "red", (left + width * 0.28, top + height * 0.18))
        self.spawn_unit("king_tower", "red", (left + width * 0.50, top + height * 0.10))
        self.spawn_unit("princess_tower", "red", (left + width * 0.72, top + height * 0.18))

        self.spawn_unit("knight", "blue", (left + width * 0.40, top + height * 0.68))
        self.spawn_unit("hogrider", "blue", (left + width * 0.60, top + height * 0.70))
        self.spawn_unit("canon", "blue", (left + width * 0.50, top + height * 0.76))

        self.spawn_unit("giant", "red", (left + width * 0.40, top + height * 0.32))
        self.spawn_unit("mini_pekka", "red", (left + width * 0.60, top + height * 0.30))
        self.spawn_unit("dart_goblin", "red", (left + width * 0.52, top + height * 0.25))

    def update(self, dt: float) -> None:
        for unit in list(self.units):
            unit.update(dt, self)

        self.units = [unit for unit in self.units if not unit.dead]

    def draw(self, screen: pygame.Surface) -> None:
        for unit in sorted(self.units, key=lambda active_unit: active_unit.position.y):
            unit.draw(screen)

    def find_target_for(self, unit: GameUnit) -> GameUnit | None:
        enemies = [enemy for enemy in self.units if enemy.camp != unit.camp and not enemy.dead]
        if not enemies:
            return None

        if unit.unit_type == "rusheur":
            buildings = [enemy for enemy in enemies if enemy.is_building]
            if buildings:
                enemies = buildings

        max_detection = self.to_pixels(8)
        if unit.is_building:
            max_detection = self.to_pixels(unit.range)

        valid_targets = [
            enemy for enemy in enemies
            if unit.distance_to(enemy) <= max_detection
        ]
        if not valid_targets:
            return None

        return min(valid_targets, key=lambda enemy: unit.distance_to(enemy))

    def damage_area(self, center: pygame.Vector2, radius: float, damage: float, source_camp: str) -> None:
        for unit in self.units:
            if unit.camp != source_camp and unit.position.distance_to(center) <= radius:
                unit.take_damage(damage)

    def default_goal_for(self, unit: GameUnit) -> pygame.Vector2:
        direction = -1 if unit.camp == "blue" else 1
        bridge_y = self.map_rect.centery + direction * self.map_rect.height * 0.06
        tower_y = self.map_rect.top + self.map_rect.height * 0.12 if unit.camp == "blue" else self.map_rect.bottom - self.map_rect.height * 0.12

        if (unit.camp == "blue" and unit.position.y > self.map_rect.centery) or (
            unit.camp == "red" and unit.position.y < self.map_rect.centery
        ):
            return pygame.Vector2(unit.position.x, bridge_y)

        return pygame.Vector2(self.map_rect.centerx, tower_y)

    def to_pixels(self, tiles: float) -> float:
        return tiles * self.tile_size

    def _load_definitions(self) -> dict[str, dict]:
        definitions = {}
        for path in Path(DEFINITIONS_PATH).glob("*.json"):
            with open(path, encoding="utf-8") as definition_file:
                data = json.load(definition_file)
            definitions[data["name"]] = data
        return definitions

    @staticmethod
    def _number(value, fallback: float) -> float:
        if value == "None" or value is None:
            return fallback
        return float(value)
