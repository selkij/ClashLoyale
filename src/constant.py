import logging
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

LOG_COLORS = {
    logging.DEBUG: '\033[36m',  # Cyan
    logging.INFO: '\033[32m',  # Green
    logging.WARNING: '\033[33m',  # Yellow
    logging.ERROR: '\033[31m',  # Red
    logging.CRITICAL: '\033[35m',  # Magenta
}
LOG_COLORS_RESET = '\033[0m'


class EventType(IntEnum):
    INPUT = auto()
    GAME = auto()


class GameEvent(StrEnum):
    START_GAME = "start_game"
