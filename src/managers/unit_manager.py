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
        self.players_by_camp = {}

    def set_players(self, blue_player, red_player) -> None:
        self.players_by_camp = {
            "blue": blue_player,
            "red": red_player,
        }

    def reset(self) -> None:
        self.units = []
        self.next_id = 1

    def spawn_unit(self, unit_name: str, camp: str, position: tuple[float, float], unit_count_override=None) -> GameUnit | None:
        unit_name = self._resolve_unit_name(unit_name)
        if unit_name not in self.definitions:
            return None

        definition = self.definitions[unit_name]
        camp = self._normalize_camp(camp)
        unit_count = unit_count_override if unit_count_override is not None else self._number(definition.get("nb_unit"), 1)
        spawned = []

        for index in range(int(unit_count)):
            offset = pygame.Vector2((index % 3) * 18, (index // 3) * 18)
            unit = GameUnit(self.next_id, definition, camp, pygame.Vector2(position) + offset)
            self.next_id += 1
            self.units.append(unit)
            spawned.append(unit)

        return spawned[0] if spawned else None

    def play_card(self, unit_name: str, camp: str, position: tuple[float, float]) -> bool:
        definition = self.get_definition(unit_name)
        if definition is None:
            return False

        if definition.get("type") == "spell":
            self.cast_spell(definition, camp, pygame.Vector2(position))
            return True

        return self.spawn_unit(unit_name, camp, position) is not None

    def get_definition(self, unit_name: str) -> dict | None:
        return self.definitions.get(self._resolve_unit_name(unit_name))

    def spawn_test_map(self) -> None:
        self.reset()
        self.spawn_default_towers()

        left = self.map_rect.left
        top = self.map_rect.top
        width = self.map_rect.width
        height = self.map_rect.height

        self.spawn_unit("knight", "blue", (left + width * 0.40, top + height * 0.68))
        self.spawn_unit("hogrider", "blue", (left + width * 0.60, top + height * 0.70))
        self.spawn_unit("canon", "blue", (left + width * 0.50, top + height * 0.76))

        self.spawn_unit("giant", "red", (left + width * 0.40, top + height * 0.32))
        self.spawn_unit("mini_pekka", "red", (left + width * 0.60, top + height * 0.30))
        self.spawn_unit("dart_goblin", "red", (left + width * 0.52, top + height * 0.25))

    def spawn_default_towers(self) -> None:
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

    def update(self, dt: float) -> None:
        for unit in list(self.units):
            unit.update(dt, self)

        for unit in list(self.units):
            if unit.dead:
                self._spawn_units_on_death(unit)

        self.units = [unit for unit in self.units if not unit.dead]

    def draw(self, screen: pygame.Surface) -> None:
        for unit in sorted(self.units, key=lambda active_unit: active_unit.position.y):
            unit.draw(screen)

    def get_winner(self) -> str | None:
        blue_king_alive = any(unit.name == "king_tower" and unit.camp == "blue" for unit in self.units)
        red_king_alive = any(unit.name == "king_tower" and unit.camp == "red" for unit in self.units)

        if blue_king_alive and red_king_alive:
            return None
        if blue_king_alive:
            return "bleu"
        if red_king_alive:
            return "rouge"
        return "egalite"

    def find_target_for(self, unit: GameUnit) -> GameUnit | None:
        unit_camp = self._normalize_camp(unit.camp)
        enemies = [
            enemy for enemy in self.units
            if enemy.id != unit.id and self._normalize_camp(enemy.camp) != unit_camp and not enemy.dead
        ]
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

    def damage_area(self, center: pygame.Vector2, radius: float, damage: float, source_camp: str, tower_damage=None, source_unit=None) -> None:
        source_camp = self._normalize_camp(source_camp)
        for unit in self.units:
            if source_unit is not None and unit.id == source_unit.id:
                continue
            if self._normalize_camp(unit.camp) != source_camp and unit.position.distance_to(center) <= radius:
                unit.take_damage(tower_damage if unit.is_building and tower_damage is not None else damage)

    def heal_area(self, center: pygame.Vector2, radius: float, healing: float, source_camp: str) -> None:
        source_camp = self._normalize_camp(source_camp)
        for unit in self.units:
            if self._normalize_camp(unit.camp) == source_camp and unit.position.distance_to(center) <= radius:
                unit.heal(healing)

    def rage_area(self, center: pygame.Vector2, radius: float, duration: float, source_camp: str) -> None:
        source_camp = self._normalize_camp(source_camp)
        for unit in self.units:
            if self._normalize_camp(unit.camp) == source_camp and unit.position.distance_to(center) <= radius:
                unit.apply_rage(duration)

    def stun_area(self, center: pygame.Vector2, radius: float, duration: float, source_camp: str) -> None:
        source_camp = self._normalize_camp(source_camp)
        for unit in self.units:
            if self._normalize_camp(unit.camp) != source_camp and unit.position.distance_to(center) <= radius:
                unit.apply_stun(duration)

    def apply_recoil_area(self, center: pygame.Vector2, radius: float, force_tiles: float, source_camp: str) -> None:
        source_camp = self._normalize_camp(source_camp)
        for unit in self.units:
            if self._normalize_camp(unit.camp) == source_camp or unit.position.distance_to(center) > radius:
                continue
            self.apply_recoil(unit, center, force_tiles)

    def apply_recoil(self, unit: GameUnit, origin: pygame.Vector2, force_tiles: float) -> None:
        effect = unit.effect if isinstance(unit.effect, dict) else {}
        resistance = self._number(effect.get("resist_recoil", effect.get("resist-recoil", 0)), 0)
        distance = max(0, force_tiles - resistance) * self.tile_size
        if distance <= 0:
            return

        direction = unit.position - origin
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)
        unit.position += direction.normalize() * distance
        unit.position.x = max(self.map_rect.left + 10, min(self.map_rect.right - 10, unit.position.x))
        unit.position.y = max(self.map_rect.top + 10, min(self.map_rect.bottom - 10, unit.position.y))

    def cast_spell(self, definition: dict, camp: str, position: pygame.Vector2) -> None:
        radius = self.to_pixels(self._number(definition.get("radius"), 1))
        damage = self._number(definition.get("damage"), 0)
        tower_damage = definition.get("tower_damage")
        tower_damage = None if tower_damage == "None" or tower_damage is None else self._number(tower_damage, damage)
        effect = definition.get("effect") if isinstance(definition.get("effect"), dict) else {}

        if definition["name"] == "log":
            self._cast_log(definition, camp, position)
            return

        spawn_units = definition.get("spawn_unit")
        if isinstance(spawn_units, list):
            for index, spawned_name in enumerate(spawn_units):
                offset = pygame.Vector2((index - 1) * 24, 20 if index == 1 else 0)
                count_override = 1 if spawned_name == "goblin_alone" else None
                self.spawn_unit(spawned_name, camp, position + offset, unit_count_override=count_override)

        if effect.get("healing"):
            self.heal_area(position, radius, self._number(effect.get("healing"), 0), camp)

        if effect.get("rage_timer"):
            self.rage_area(position, radius, self._number(effect.get("rage_timer"), 0), camp)

        if damage > 0:
            self.damage_area(position, radius, damage, camp, tower_damage=tower_damage)

        if effect.get("stunt"):
            self.stun_area(position, radius, self._number(effect.get("stunt"), 0), camp)

        if effect.get("recoil"):
            self.apply_recoil_area(position, radius, self._number(effect.get("recoil"), 0), camp)

    def add_elixir(self, camp: str, amount: float) -> None:
        player = self.players_by_camp.get(camp)
        if player is not None:
            player.modify_elixir(amount)

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

    def _cast_log(self, definition: dict, camp: str, position: pygame.Vector2) -> None:
        direction = -1 if camp == "blue" else 1
        length = self.to_pixels(self._number(definition.get("radius"), 12))
        width = self.to_pixels(1.8)
        start_y = position.y
        end_y = position.y + direction * length
        min_y = min(start_y, end_y)
        rect = pygame.Rect(position.x - width / 2, min_y, width, abs(end_y - start_y))
        damage = self._number(definition.get("damage"), 0)
        effect = definition.get("effect") if isinstance(definition.get("effect"), dict) else {}

        for unit in self.units:
            if unit.camp != camp and rect.collidepoint(unit.position):
                unit.take_damage(damage)
                if effect.get("recoil"):
                    self.apply_recoil(unit, pygame.Vector2(position.x, start_y - direction * 40), self._number(effect.get("recoil"), 0))

    def _spawn_units_on_death(self, unit: GameUnit) -> None:
        spawn_units = unit.definition.get("spawn_unit")
        if not isinstance(spawn_units, list):
            return
        if unit.death_spawned:
            return

        unit.death_spawned = True

        for index, spawned_name in enumerate(spawn_units):
            offset = pygame.Vector2((index - 0.5) * 28, 0)
            self.spawn_unit(spawned_name, unit.camp, unit.position + offset)

    def _resolve_unit_name(self, unit_name: str) -> str:
        aliases = {
            "goblin_alone": "goblin",
            "min_golem": "min_golem",
            "mini_golem": "min_golem",
            "elixir_pump": "elexir_pump",
            "inferno_tower": "infernal_tower",
        }
        return aliases.get(unit_name, unit_name)

    def _load_definitions(self) -> dict[str, dict]:
        definitions = {}
        for path in sorted(Path(DEFINITIONS_PATH).glob("*.json")):
            with open(path, encoding="utf-8") as definition_file:
                data = json.load(definition_file)
            definitions[path.stem] = data
            if data["name"] == path.stem or data["name"] not in definitions:
                definitions[data["name"]] = data

        definitions["elixir_pump"] = definitions["elexir_pump"]
        definitions["inferno_tower"] = definitions["infernal_tower"]
        return definitions

    @staticmethod
    def _normalize_camp(camp: str) -> str:
        aliases = {
            "bleu": "blue",
            "rouge": "red",
        }
        return aliases.get(camp, camp)

    @staticmethod
    def _number(value, fallback: float) -> float:
        if value == "None" or value is None:
            return fallback
        return float(value)
