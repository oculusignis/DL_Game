import pygame
import random


class ColorBox(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.screen = (x, y)
        self.image = pygame.Surface((50, 50))
        self.image.fill((230, 100, 100))
        self.rect = self.image.get_rect()

        self.move()

    def move(self):
        """moves the ColorBox to a random place on the screen"""
        self.rect.topleft = (random.randint(0, self.screen[0] - 50), random.randint(0, self.screen[1] - 50))
