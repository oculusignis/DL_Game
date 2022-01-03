import pygame
from spriteSheet import SpriteSheet

orientationLib = {'idle': 0, 'right': 1, 'down': 2, 'left': 3, 'up': 4, 'death': 5}
js_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}
# TODO dash bar somewhere on the screen
# TODO health bar


# Define player object as extension of pygame.sprite.Sprite
# Surface drawn on screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    """Player Object, controlled by WASD and SPACE"""

    def __init__(self, player_number: int, mult: int, screen: pygame.Surface, framerate: int):
        """Initialize Player with the scaling Multiplier"""
        super().__init__()
        # general game data
        self.screen = screen
        self.size_multiplier = mult
        self.framerate = framerate
        self.js = pygame.joystick.Joystick(player_number)

        # player attributes
        self.xy_change = [0, 0]
        self.base_speed = 4
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.status = {"alive": 1, "dashing": False, "attacking": False, "invulnerable": False}
        self.dash_counter = 1000

        # init image and rect
        self.ss = SpriteSheet('resources/Sam66_22-28.png')
        self.image = self.getspriteimage()
        self.rect = self.image.get_bounding_rect()
        self.center = (self.screen.get_width() / 2, self.screen.get_height() - self.screen.get_height() / 8)
        self.move(self.center)

        # init hitboxes
        self.hitbox = pygame.rect.Rect(self.center[0] + 11*mult, self.center[1] + 11*mult, 22*mult, 22*mult)  # TODO
        self.sword = Sword(mult)

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
        y = orientationLib[self.orientation] * sizey
        return pygame.transform.scale(self.ss.image_at((x, y, sizex, sizey), -1),
                                      (sizex*self.size_multiplier, sizey*self.size_multiplier)).convert_alpha()

    def move(self, loc=(0, 0)):
        """moves character to loc coordinates"""
        self.rect.center = loc

    def walk(self, dt):
        """normal walk animation"""
        # clear variables
        self.xy_change = [0, 0]

        # determine change of coordinates
        axes = [round(self.js.get_axis(0)), round(self.js.get_axis(1))]
        self.xy_change = axes

        # calculate speed
        speed = self.base_speed * dt
        if self.xy_change[0] != 0 and self.xy_change[1] != 0:
            speed *= 0.9

        # move the rect
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

    def update(self, dt):
        """update Player sprite"""
        screenw, screenh = self.screen.get_size()
        if self.status["alive"] > 0:
            # dash or (walk and charge dash)?
            startdash = all((self.js.get_button(js_lib["B"]), self.dash_counter == 1000, self.orientation != "idle"))
            startattack = all((self.js.get_button(js_lib["A"]), True))  # TODO attack counter instead of True
            if self.status["dashing"] or startdash:
                self.dash(dt)
            elif self.status["attacking"] or startattack:
                self.attack(dt)
            else:
                self.walk(dt)
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


class Sword(pygame.sprite.Sprite):
    """handles the rect for the sword hitbox"""
    def __init__(self, mult):
        # general data
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
