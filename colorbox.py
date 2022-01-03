import pygame
import random


class ColorBox(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((50, 50))
        self.image.fill((230, 100, 100))
        self.rect = self.image.get_rect()

        self.move()

    def reset(self):
        self.move()

    def move(self):
        """moves the ColorBox to a random place on the screen"""
        size = self.screen.get_size()
        self.rect.topleft = (random.randint(0, size[0] - 50), random.randint(0, size[1] - 50))
