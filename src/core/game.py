import pygame


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock() # UI class MUST be instantiated first
        self.running = True
        self.dt = 0

    def tick(self):
        # Limits FPS to 60
        self.dt = self.clock.tick(60) / 1000.0
