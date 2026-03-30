import logging

import pygame
import os

import constant
from utils import log

class Sound:
    def __init__(self):
        pygame.mixer.init()
        log.logger.send("Initialized sound system", logging.DEBUG)

    # Music
    def play_music(self, filename):
        """Load and play a music file once."""
        path = constant.SOUNDS_PATH / filename
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()  # joue une fois
        log.logger.send(f"played {filename}", logging.DEBUG)

        return path  # retourne le path si besoin

    def loop_music(self):
        """Loop the currently loaded music infinitely."""
        if pygame.mixer.get_busy():
            pygame.mixer.music.play(loops=-1)
            log.logger.send("Set current music as looped infinitely.", logging.DEBUG)
        else:
            log.logger.send("No music is playing, cannot loop.", logging.WARNING)


    def stop_music(self):
        """Stop the currently playing music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            log.logger.send("Stopped current music.", logging.DEBUG)
        else:
            log.logger.send("No music is playing, cannot stop.", logging.WARNING)

    def rewind_music(self):
        """Rewind the currently playing music."""
        if not pygame.mixer.get_busy():
            log.logger.send("No music is playing, cannot rewind.", logging.WARNING)
        else:
            pygame.mixer.music.rewind()
            log.logger.send("Rewinded current music.", logging.DEBUG)

    # SFX
    def start_sfx(self, filename):
        """Play a SFX once or use loop() to loop it."""
        sfx = constant.SOUNDS_PATH / filename
        sfx = pygame.mixer.Sound(sfx)
        sfx.play()  # joue une fois
        log.logger.send(f"played sfx {filename}", logging.DEBUG)
        return sfx  # retourne l'objet Sound pour pouvoir le boucler plus tard

    def loop_sfx(self, sfx):
        """Loop a sound infinitely."""
        sfx.play(loops=-1)

