import pygame
import os
from utils import log
import logging

pygame.init()
pygame.mixer.init()

def start_sfx(filename):
    """Play a SFX once or use loop() to loop it."""
    base_dir = os.path.dirname(__file__)
    sound_path = os.path.join(base_dir, "..", "sounds", filename)
    sound = pygame.mixer.Sound(sound_path)
    sound.play()  # joue une fois
    log.logger.send(f"played {filename}", logging.DEBUG)
    return sound  # retourne l'objet Sound pour pouvoir le boucler plus tard


def loop(sound):
    """Loop a sound infinitely."""
    sound.play(loops=-1)
