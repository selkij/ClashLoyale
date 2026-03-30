import sys
import traceback

import pygame
import logging

from utils import log

log.Logger('debug.log', logging.INFO) # Will directly populate the logger variable
log.logger.send("Setting game definitions", logging.DEBUG)


def close_game(is_error = False):
    log.logger.send("Closing game...", logging.DEBUG)
    pygame.quit()

    # Prevent further execution
    if is_error:
        sys.exit(-1)
    sys.exit(0)

# Pygame setup
try:
    log.logger.send("Clash Loyale is ready ! hehehehaw", logging.INFO)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Module tick functions here

    close_game()
except Exception:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_list = traceback.format_exception(exc_type, exc_value, exc_traceback)

    for line in tb_list:
        clean_line = line.replace("\n", "")
        log.logger.send(clean_line, logging.CRITICAL)
    traceback.print_exc()
    close_game(True)


pygame.quit()
