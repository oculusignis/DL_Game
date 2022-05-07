import pygame
import config
import math

edge1 = 1.1 * math.pi

sprite_size = (22, 28)

orientationLib = {'idle': 0, 'right': 1, 'down': 2, 'left': 3, 'up': 4, 'death': 5}
js_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}

axis2ori = {(0, -1): 'up',
            (0, 0): 'idle',
            (0, 1): 'down',
            (1, -1): 'right',
            (1, 0): 'right',
            (1, 1): 'right',
            (-1, -1): 'left',
            (-1, 0): 'left',
            (-1, 1): 'left'}


# TODO health bar


# Define player object as extension of pygame.sprite.Sprite
# Surface drawn on screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    """player controlled Sprite"""

    def __init__(self, player_number: int):
        """Initialize Player with the players number"""
        super().__init__()
        # general game sdata
        self.js = pygame.joystick.Joystick(player_number)

        # player attributes
        self.xy_change = pygame.math.Vector2(0.0, 0.0)
        self.speed_base = 4
        self.stamina = 1000
        self.stamina_regen = 1
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.status = {"alive": 1, "dashing": False, "attacking": False, "invulnerable": False}  # TODO remove dashing
        self.pos = pygame.math.Vector2(config.screen.get_width() / 2,
                                       config.screen.get_height() - config.screen.get_height() / 8)

        # init image and rect
        self.ss = config.sheet_player
        self.image = self.getspriteimage()
        self.rect = self.image.get_bounding_rect()
        self.move(self.pos)

        # dash variables
        self.dash_len = 25
        self.dash_counter = 0
        self.dash_rect = pygame.rect.Rect(self.pos.x + 11 * config.sizer, self.pos.y + 11 * config.sizer,
                                          5 * config.sizer, 5 * config.sizer)
        self.dash_surf = pygame.Surface(self.dash_rect.size)
        pygame.draw.arc(self.dash_surf, (0, 0, 0), self.dash_rect, math.pi, 2 * math.pi)

        # init hitboxes
        self.hitbox = pygame.rect.Rect(self.pos.x + 11 * config.sizer, self.pos.y + 11 * config.sizer,
                                       22 * config.sizer, 22 * config.sizer)  # TODO

    def reset(self):
        """player reset for start of game"""
        self.xy_change = [0, 0]
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.image = self.getspriteimage()
        self.stamina = 1000
        self.dash_counter = 0
        self.move((config.screen.get_width() / 2, config.screen.get_height() - config.screen.get_height() / 8))
        self.status = {"alive": 1, "dashing": False, "attacking": False, "invulnerable": False}

    def getspriteimage(self):
        """produces a pygame image from the spritesheet"""
        sizex = 22
        sizey = 28
        x = self.move_info["move"] * sizex
        y = orientationLib[self.orientation] * sizey
        return pygame.transform.scale(self.ss.image_at((x, y, sizex, sizey), -1),
                                      (sizex * config.sizer, sizey * config.sizer)).convert_alpha()

    def move(self, loc=(0, 0)):
        """moves character to loc coordinates"""
        self.pos.update(loc)
        self.rect.center = loc

    def walk(self, dt):
        """normal walk animation"""
        # get controller_axis
        self.xy_change = pygame.math.Vector2(round(self.js.get_axis(0)), round(self.js.get_axis(1)))

        # Determine Character orientation
        old_orientation = self.orientation
        self.orientation = axis2ori[(round(self.xy_change.x), round(self.xy_change.y))]

        # determine change of coordinates
        if self.xy_change.length_squared() > 0:
            speed = self.speed_base * dt
            self.xy_change.scale_to_length(speed)
            self.pos += self.xy_change

        # Determine sprite move
        if self.orientation == old_orientation:
            self.move_info["time"] += dt
            # increase move number if more than a 1/4 s passed
            if self.move_info["time"] > config.framerate / 4:
                self.move_info["move"] = self.move_info["move"] + 1 if self.move_info["move"] < 3 else 0
                self.move_info["time"] = 0
        else:
            self.move_info["time"] = 0
            self.move_info["move"] = 0

        # Sprite move and number determined, get the image
        self.image = self.getspriteimage()

    def dash(self, dt):
        """dash movement"""
        self.dash_counter = (self.dash_counter + 1) % self.dash_len  # increase dash counter
        speed = 2.5 * self.speed_base * dt  # dash speed
        self.xy_change.scale_to_length(speed)
        self.pos += self.xy_change

    def death(self, dt):
        """death animation"""
        self.move_info["time"] += dt
        # increase move number if more than a 1/4 s passed
        if self.move_info["time"] > config.framerate / 4:
            self.move_info["move"] = self.move_info["move"] + 1
            self.move_info["time"] = 0
            if self.move_info["move"] < 4:
                self.image = self.getspriteimage()
            else:
                self.status["alive"] = -1

    def attack(self, dt):
        """attack animation"""
        self.move_info["time"] += dt

    def update(self, dt):
        """update Player sprite"""
        if self.status["alive"] > 0:
            # dash or (walk and charge dash)?
            startdash = all((self.js.get_button(js_lib["B"]), self.stamina > 200, self.orientation != "idle"))
            startattack = all((self.js.get_button(js_lib["A"]), True))  # TODO attack counter instead of True

            if self.dash_counter:
                self.dash(dt)
            elif startdash:
                self.stamina -= 200
                self.dash(dt)
            elif self.status["attacking"] or startattack:
                self.attack(dt)
            else:
                self.walk(dt)
                if self.stamina < 1000:
                    self.stamina += self.stamina_regen

            # keep player in screen
            x_margin = sprite_size[0] / 2 * config.sizer
            y_margin = sprite_size[1] / 2 * config.sizer

            if self.pos.x < x_margin:
                self.pos.x = x_margin
            elif self.pos.x > config.screen.get_width() - x_margin:
                self.pos.x = config.screen.get_width() - x_margin

            if self.pos.y < y_margin:
                self.pos.y = y_margin
            elif self.pos.y > config.screen.get_height() - y_margin:
                self.pos.y = config.screen.get_height() - y_margin

            # Move Player rect to current position
            self.rect.center = round(self.pos.x), round(self.pos.y)

        elif self.status["alive"] == 0:
            self.orientation = 'death'
            self.death(dt)


class Sword(pygame.sprite.Sprite):
    """handles the rect for the sword hitbox"""

    def __init__(self, mult):
        # general sdata
        super().__init__()
        self.mult = mult
        self.rect = pygame.rect.Rect(-1, -1, 1, 1)

    def reset(self):
        """puts sword rect outside of screen, so no collisions happen"""
        self.rect.update(-1, -1, 1, 1)

    def up(self, center):
        """puts sword rect above the player"""
        self.rect.size = (42 * self.mult, 10 * self.mult)
        self.rect.center = (center[0], center[1] + 16 * self.mult)

    def down(self, center):
        """puts sword rect below the player"""
        self.rect.size = (42 * self.mult, 10 * self.mult)
        self.rect.center = (center[0], center[1] - 16 * self.mult)

    def right(self, center):
        """puts sword rect right of the player"""
        self.rect.size = (10 * self.mult, 42 * self.mult)
        self.rect.center = (center[0] + 16, center[1])

    def left(self, center):
        """puts sword rect left of the player"""
        self.rect.size = (10 * self.mult, 42 * self.mult)
        self.rect.center = (center[0] - 16, center[1])
