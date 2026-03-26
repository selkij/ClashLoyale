import logging

import pygame
import os

from utils import log


def sound_init():
    """Initialize the mixer."""
    pygame.mixer.init()
    log.logger.send("Initialized sound system", logging.DEBUG)

def play_music(filename):
    """Load and play a music file once."""
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "themes", filename)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()  # joue une fois
    log.logger.send(f"played {filename}", logging.DEBUG)

    return path  # retourne le path si besoin

def loop_music():
    """Loop the currently loaded music infinitely."""
    pygame.mixer.music.play(loops=-1)

def stop_music():
    """Stop the currently playing music."""
    pygame.mixer.music.stop()

def rewind_music():
    """Rewind the currently playing music."""
    if not pygame.mixer.get_busy():
        print("Music is not playing!")
    else:
        pygame.mixer.music.rewind()
