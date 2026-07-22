from constant import UNIT_SOUNDS_PATH
from core.sound import Sound
from managers.Unit.abilities.attack import Attack
from managers.Unit.game_unit import GameUnit
from utils.path_animate import unit_animation


class Pekka(GameUnit):
    def __init__(self, modules: dict, unit_id: int, camp: str, properties: dict, pos: tuple):
        super().__init__(modules, camp, unit_id, properties, pos)
        sound_module: Sound = self.modules["sound"]

        self.add_ability(
            Attack(modules["sound"], damage=self._properties["damage"], attacks_per_second=self._properties["freq_atk"],
                   attack_range=self._properties["range"], sfx=UNIT_SOUNDS_PATH / "pekka-hit.wav"))

        sound_module.play_sound(UNIT_SOUNDS_PATH / "pekka-deploy.wav") # Spawn sfx

        self._animator.register_animation("stand", unit_animation(self.name, "stand", camp, 1, True))
        self._animator.register_animation("hit", unit_animation(self.name, "hit", camp, 0.15))
        self._animator.register_animation("run", unit_animation(self.name, "run", camp, 1, True))
        self._animator.play("stand")

    def on_update(self, dt: float, enemies: list[GameUnit]):
        if len(enemies) != 0:
            nearest = min(enemies, key=lambda x: x.distance_to(self.pos))  # Gets the closest enemy to the unit.
            self.use_ability("attack", nearest)
