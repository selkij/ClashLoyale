# All of this are just example usages of different parts of the game.
import pygame
import music.music
from music.music import sound_init, start_music, combat_theme, deck_theme
from music.sfx import hog_rider_sfx

# Pygame setup
pygame.init()
pygame.font.init()

pygame.display.set_caption("Clash Loyale")
icon = pygame.image.load("sprites/game_icon.png") # PyInstaller ?
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()

running = True
dt = 0

# Game variables
background_color = "#202020"
text_color = "#EEEEEE"
green_land_color = "#55D930"
green_land_alt_color = "#4CC72A"
path_land_color = "#F8B03C"
path_land_alt_color = "#E0A036"
river_color = "#00A8BD"

arena_img = pygame.image.load("sprites/arena.png").convert()
arena_img_size = arena_img.get_size()
arena_img = pygame.transform.scale(arena_img, (screen.get_width()/2, screen.get_height()))

font = pygame.font.Font('fonts/YouBlockhead.ttf', 40)
title_text = font.render('Thomate', True, text_color)
title_rect = title_text.get_rect()

screen.fill(background_color)
screen.blit(arena_img, (screen.get_width()/2-arena_img.get_size()[0]/2, 0))
screen.blit(title_text, title_rect)
pygame.display.flip()

# base initialisation
sound_init()
#deck_theme()
combat_theme()
#hog_rider_sfx()
#  actually running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.display.flip()

    # Limits FPS to 60
    dt = clock.tick(60) / 1000


pygame.quit()
