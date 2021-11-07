import pygame


class TestSprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/testSprite/left.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)
        self.counter = 0
        self.pos = True

    def update(self, *args, **kwargs) -> None:
        self.counter += 1

        if self.counter > 150:
            self.counter = 0
            if self.pos:
                self.image = pygame.image.load("resources/testSprite/right.png").convert()
                self.pos = False
            else:
                self.image = pygame.image.load("resources/testSprite/left.png").convert()
                self.pos = True
