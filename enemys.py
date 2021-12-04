import pygame


class Enemy1(pygame.sprite.Sprite):
    """Basic Enemy Object, walks to Player"""

    def __init__(self, mult):
        super().__init__()
        self.size_multiplier = mult
        self.image = pygame.image.load('resources/rectSprite/center.png')
        self.rect = self.image.get_rect()
        self.area = pygame.Rect((0, 0, 100, 100))
        self.area.center = self.rect.center
        self.following = None
        self.speed = 2

    def reset(self):
        self.rect.topleft = (0, 0)

    def update(self, player, dt):

        # TODO calculate distance from ALL Players and follow closest one
        if player.status["alive"] > 0:
            vector = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                         player.rect.centery - self.rect.centery)

            if vector.length() < 10:
                pass
            elif vector.length() < 700:
                vector.normalize_ip()
                vector.scale_to_length(self.speed)
                # if abs(vector.x) > 1 and abs(vector.y) > 1:
                #     print("diagonal")
                self.rect.move_ip(vector)
