import pygame

import constant
from utils import log


def auto_scaling():
    """
    Returns the physical window size and the ratio used to fit the logical
    game resolution inside the current screen.
    """

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    base_w = constant.SCREEN_WIDTH
    base_h = constant.SCREEN_HEIGHT

    log.logger.send(f"Size of the window {screen_w}x{screen_h}", constant.TRACE)

    scale_w = screen_w / base_w
    scale_h = screen_h / base_h

    scale = max(0.01, min(scale_w, scale_h, 1))
    window_w = max(1, int(base_w * scale))
    window_h = max(1, int(base_h * scale))

    log.logger.send(
        f"Auto scale ratio {scale:.3f}: logical {base_w}x{base_h}, window {window_w}x{window_h}",
        constant.TRACE
    )

    return window_w, window_h, scale
