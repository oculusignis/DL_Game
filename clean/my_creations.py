import pygame


class Basic(pygame.sprite.Sprite):
    """basic object"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([80, 50])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(50, 50)
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def update(self, orientation=pygame.math.Vector2(0, 0)):
        if orientation.length_squared() > 0:
            orientation.scale_to_length(1)
            self.pos += orientation
            self.rect.center = round(self.pos.x), round(self.pos.y)
