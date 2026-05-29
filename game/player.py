import pygame

from game.config import Position

ANIMATION_DURATION_MS = 40


class Player:
    def __init__(self):
        self.position = Position.RIGHT
        self.chopping = False
        self._animation_timer = 0

    def reset(self):
        self.position = Position.RIGHT
        self.chopping = False
        self._animation_timer = 0

    def chop(self, position: Position):
        self.position = position
        self.chopping = True
        self._animation_timer = pygame.time.get_ticks()

    def update(self):
        if self.chopping and pygame.time.get_ticks() - self._animation_timer > ANIMATION_DURATION_MS:
            self.chopping = False
