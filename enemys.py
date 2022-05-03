import pygame
import mcreations
import config

range = 700
difficulty_scaling = 0.025


class Enemy1(mcreations.Entity):
    """Basic Enemy Object, walks to Player"""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('resources/rectSprite/center.png')
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.copy()
        # self.area = pygame.Rect((0, 0, 100, 100))
        # self.area.center = self.rect.center
        self.pos = pygame.math.Vector2(8, 8)
        self.following = None
        self.speed = 2

    def move(self, loc):
        self.pos.xy = loc
        self.rect.center = loc
        self.hitbox.center = loc

    def reset(self):
        self.move((8, 8))

#    def update(self, dt, *args):
#        """update Enemy1 for a single Player"""
#        player = args[0]
#        vector2p = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
#
#        if range > vector2p.length() > 10:
#            vector2p.normalize_ip()
#            vector2p.scale_to_length(self.speed*dt + config.score*difficulty_scaling)
#            self.pos += vector2p
#            self.rect.center = round(self.pos.x), round(self.pos.y)
#            self.hitbox.center = self.rect.center

    def update(self, dt, *args):
        """update Enemy1 in Multiplayer"""
        # calculate closest player
        players = args[0]
        closest_player = (range, pygame.math.Vector2(0, 0))  # distance, Vector
        for p in players:
            if p.status["alive"] > 0:
                vector2p = pygame.math.Vector2(p.rect.centerx - self.rect.centerx, p.rect.centery - self.rect.centery)
                vector_l = vector2p.length()
                if vector_l < closest_player[0]:
                    closest_player = (vector_l, vector2p)

        # move to closest player
        if range > closest_player[0] > 10:
            closest_player[1].normalize_ip()
            closest_player[1].scale_to_length(self.speed*dt + config.score*difficulty_scaling)

            self.pos += closest_player[1]
            self.rect.center = round(self.pos.x), round(self.pos.y)
            self.hitbox.center = self.rect.center
