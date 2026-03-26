import sys

import pygame
import logging

import input
import settings
from music.music import sound_init, play_music
from utils import log

log.Logger('debug.log', logging.DEBUG) # Will directly populate the logger variable
log.logger.send("Setting game definitions", logging.DEBUG)
settings.init(900, 900)

log.logger.send("Initializing pygame", logging.DEBUG)

def close_game(is_error = False):
    log.logger.send("Closing game...", logging.DEBUG)
    pygame.quit()

    # Prevent further execution
    if is_error:
        sys.exit(-1)
    sys.exit(0)

# Pygame setup
try:
    pygame.init()
    input.init()
    pygame.font.init()

    sound_init()

    pygame.display.set_caption("Clash Loyale")
    icon = pygame.image.load("sprites/game_icon.png") # PyInstaller ?
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    clock = pygame.time.Clock()

    running = True
    dt = 0

    # Game variables
    background_color = "#202020"
    text_color = "#EEEEEE"

    log.logger.send("Loading assets", logging.DEBUG)

    arena_img = pygame.image.load("sprites/arena.png").convert()
    arena_img_size = arena_img.get_size()
    arena_img = pygame.transform.scale(arena_img, (screen.get_width()/2, screen.get_height()))

    font = pygame.font.Font('fonts/YouBlockhead.ttf', 40)
    title_text = font.render('Thomate', True, text_color)
    title_rect = title_text.get_rect()

    log.logger.send("Drawing arena", logging.DEBUG)
    screen.fill(background_color)
    screen.blit(arena_img, (screen.get_width()/2-arena_img.get_size()[0]/2, 0))
    screen.blit(title_text, title_rect)
    pygame.display.flip()

    start_sound = pygame.mixer.Sound("sounds/spawn_hog_rider.mp3")
    start_sound.play()

    log.logger.send("Clash Loyale is ready ! hehehehaw", logging.INFO)


    play_music("combat.mp3")

    while running:
        for event in pygame.event.get():
            # Sub-systems event handling
            input.handle_events(event)

            if event.type == pygame.QUIT:
                running = False

        # pygame.display.flip()

        # Limits FPS to 60
        dt = clock.tick(60) / 1000

    close_game()
except pygame.error as e:
    log.logger.send(e, logging.CRITICAL)
    close_game(True)

pygame.quit()
