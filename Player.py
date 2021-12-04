import pygame
from spriteSheet import SpriteSheet
from pygame.locals import (
    # RLEACCEL,
    K_SPACE,
    K_w,
    K_a,
    K_s,
    K_d
)

# TODO dash bar somewhere on the screen


# Define player object as extension of pygame.sprite.Sprite
# Surface drawn on screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    """Player Object, controlled by WASD and SPACE"""

    def __init__(self, mult, screen: pygame.display, framerate):
        """Initialize Player with the scaling Multiplier"""
        super().__init__()
        self.screen = screen
        self.size_multiplier = mult
        self.framerate = framerate
        self.click = False
        self.xy_change = [0, 0]
        self.base_speed = 4
        self.orientation = 'idle'
        self.orientationLib = {'idle': 0, 'right': 1, 'down': 2, 'left': 3, 'up': 4, 'death': 5}
        self.move_info = {"time": 0, "move": 0}
        self.status = {"alive": 1, "dashing": False, "attacking": False, "invulnerable": False}
        self.dash_counter = 1000
        self.ss = SpriteSheet('resources/Sam66_22-28.png')
        self.image = self.getspriteimage()
        self.rect = self.image.get_bounding_rect()
        self.move((self.screen.get_width() / 2, self.screen.get_height() - self.screen.get_height() / 8))

    def reset(self):
        self.xy_change = [0, 0]
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.dash_counter = 1000
        self.move((self.screen.get_width() / 2, self.screen.get_height() - self.screen.get_height() / 8))
        self.status = {"alive": 1, "dashing": False, "attacking": False, "invulnerable": False}

    def getspriteimage(self):
        """produces a pygame image from the spritesheet"""
        sizex = 22
        sizey = 28
        x = self.move_info["move"] * sizex
        y = self.orientationLib[self.orientation] * sizey
        x = pygame.transform.scale(self.ss.image_at((x, y, sizex, sizey), -1),
                                   (sizex*self.size_multiplier, sizey*self.size_multiplier)).convert_alpha()

        return x    # TODO crop rectangle to surface

    def move(self, loc=(0, 0)):
        """moves character to loc coordinates"""
        self.rect.center = loc

    def walk(self, press_k, dt):
        """normal walk animation"""
        # clear variables
        self.xy_change = [0, 0]

        # determine change of coordinates
        if press_k[K_a]:
            self.xy_change[0] -= 1
        if press_k[K_d]:
            self.xy_change[0] += 1
        if press_k[K_w]:
            self.xy_change[1] -= 1
        if press_k[K_s]:
            self.xy_change[1] += 1

        # calculate speed
        speed = self.base_speed * dt
        if self.xy_change[0] != 0 and self.xy_change[1] != 0:
            speed *= 0.9

        # move character
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
            self.click = False
        else:
            self.rect.move_ip(self.xy_change[0] * speed, self.xy_change[1] * speed)

        # Determine Character orientation
        old_orientation = self.orientation
        if self.xy_change[1] < 0:
            self.orientation = "up"
        elif self.xy_change[1] > 0:
            self.orientation = "down"

        if self.xy_change[0] < 0:
            self.orientation = "left"
        elif self.xy_change[0] > 0:
            self.orientation = "right"
        if self.xy_change[0] == 0 and self.xy_change[1] == 0:
            self.orientation = "idle"

        # Determine sprite move
        if self.orientation == old_orientation:
            self.move_info["time"] += dt
            # increase move number if more than a 1/4 s passed
            if self.move_info["time"] > self.framerate / 4:
                self.move_info["move"] = self.move_info["move"] + 1 if self.move_info["move"] < 3 else 0
                self.move_info["time"] = 0
        else:
            self.move_info["time"] = 0
            self.move_info["move"] = 0

        # Sprite move and number determined, get the image
        self.image = self.getspriteimage()

    def dash(self, dt):
        """dash animation"""
        self.dash_counter -= 50          # increase dash counter
        if self.dash_counter == 0:
            self.status["dashing"] = False
        else:
            self.status["dashing"] = True
        speed = 2.5 * self.base_speed * dt   # dash speed
        self.rect.move_ip(self.xy_change[0] * speed, self.xy_change[1] * speed)

    def death(self, dt):
        """death animation"""
        self.move_info["time"] += dt
        # increase move number if more than a 1/4 s passed
        if self.move_info["time"] > self.framerate / 4:
            self.move_info["move"] = self.move_info["move"] + 1
            self.move_info["time"] = 0
            if self.move_info["move"] < 4:
                self.image = self.getspriteimage()
            else:
                self.status["alive"] = -1

    def attack(self, dt):
        """attack animation"""
        self.move_info["time"] += dt

    def update(self, press_k, screenw: int, screenh: int, dt):
        """update Player sprite"""
        if self.status["alive"] > 0:
            # dash or (walk and charge dash)?
            startdash = all((press_k[K_SPACE], self.dash_counter == 1000, self.orientation != "idle"))
            if self.status["dashing"] or startdash:
                self.dash(dt)
            else:
                self.walk(press_k, dt)
                if self.dash_counter < 1000:
                    self.dash_counter += 1

            # keep player in screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screenw:
                self.rect.right = screenw
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screenh:
                self.rect.bottom = screenh

        elif self.status["alive"] == 0:
            self.orientation = 'death'
            self.death(dt)
