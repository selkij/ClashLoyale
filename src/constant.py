from enum import auto, IntEnum, StrEnum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SOUNDS_PATH = BASE_DIR / "sounds"
MUSIC_THEMES_PATH = SOUNDS_PATH / "themes"
SPRITES_PATH = BASE_DIR / "sprites"
FONTS_PATH = BASE_DIR / "fonts"

TEXT_COLOR = "#EEEEEE"
BACKGROUND_COLOR = "#202020"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


class EventType(IntEnum):
    INPUT = auto()
    GAME = auto()


class GameState(IntEnum):
    MENU = 1
    DECK_SELECTION = 2
    GAME = 3
    PAUSED = 4
    END_GAME = 5
    EXIT = 6


class GameEvent(StrEnum):
    START_GAME = "start_game"
