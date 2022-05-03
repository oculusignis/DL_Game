import pygame
import math
import random
import config

# -------------------------------------------------------------------------------------------------------
# Variables
# -------------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------------
# General classes and functions
# -------------------------------------------------------------------------------------------------------


class Entity(pygame.sprite.Sprite):
    """Meant for all game objects"""

    def __int__(self):
        self.hitbox = pygame.rect.Rect(0, 0, 1, 1)
        self.pos = pygame.Vector2(0, 0)

    def move(self, loc: (float, float)):
        """move entitiy to loc coordinates"""
        self.pos.xy = loc
        self.rect.center = loc
        self.hitbox.center = loc

    def reset(self):
        pass

    def update(self, dt, *args):
        pass


class Character(Entity):
    """Entity with abilities"""

    def getspriteimage(self):
        """produces a pygame image from the spritesheet"""
        pass

    def attack(self, dt):
        pass

    def death(self, dt):
        pass


class EntityGroup:
    """group of entities, whose members can act collectively or be iterated upon"""

    def __init__(self, *entities: Entity):
        self._members = list(entities)

    def __len__(self):
        return len(self._members)

    def __iter__(self):
        return (ent for ent in self._members)

    def add(self, *new_ent):
        """Add the given Entities to the group"""
        for ent in new_ent:
            self._members.append(ent)

    def remove(self, *rem_ent):
        """remove the given Entities from the group"""
        for ent in rem_ent:
            self._members.remove(ent)

    def update(self, dt, *args):
        """Update all group members"""
        for ent in self._members:
            ent.update(dt, args[0])

    def draw(self, surface: pygame.Surface):
        """Draw all group members on the surface"""
        for ent in self._members:
            surface.blit(ent.image, ent.rect)

    def reset(self):
        """Resets all members of the group"""
        for ent in self._members:
            ent.reset()


class CharacterGroup(EntityGroup):
    """Works like EntityGroup but with Characters"""

    def __init__(self, *characters: Character):
        super(CharacterGroup, self).__init__()
        self._members = list(characters)


def collisions(entity: Entity, group: EntityGroup):
    """finds all group members, that intersect with the given entity"""
    c = [group_member for group_member in group if entity.hitbox.colliderect(group_member.hitbox)]
    return c


# -------------------------------------------------------------------------------------------------------
# specific Classes
# -------------------------------------------------------------------------------------------------------

#
class ColorBox(Entity):
    """test target entitiy"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((230, 100, 100))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.copy()

        self.move()

    def reset(self):
        self.move()

    def move(self, *args):
        """moves the ColorBox to a random place on the screen"""
        size = config.screen.get_size()
        loc = (random.randint(0, size[0] - 50), random.randint(0, size[1] - 50))
        self.rect.topleft = loc
        self.hitbox.topleft = loc


# Define player object as extension of Character
# Surface drawn on screen is now an attribute of 'player'
class Player(Character):
    """player controlled Sprite"""

    def __init__(self, player_number: int):
        """Initialize Player with the players number"""
        super().__init__()
        # general game data
        self.js = pygame.joystick.Joystick(player_number)

        # player attributes
        self.xy_change = pygame.math.Vector2(0.0, 0.0)
        self.speed_base = 4
        self.stamina = 1000
        self.stamina_regen = 1
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.status = {"alive": 1, "dashed": False, "attacking": False, "invulnerable": False}
        self.pos = pygame.math.Vector2(config.screen.get_width() / 2,
                                       config.screen.get_height() - config.screen.get_height() / 8)

        # init image and rect
        self.ss = config.sheet_player
        self.image = self.getspriteimage()
        self.rect = self.image.get_bounding_rect()

        # init hitboxes
        self.hitbox = self.rect.copy()

        self.move(self.pos)

        # dash variables
        self.dash_len = 25
        self.dash_counter = 0
        self.dash_rect = pygame.rect.Rect(self.pos.x + 11 * config.sizer, self.pos.y + 11 * config.sizer,
                                          5 * config.sizer, 5 * config.sizer)
        self.dash_surf = pygame.Surface(self.dash_rect.size)

    def reset(self):
        """player reset for start of game"""
        self.xy_change = [0, 0]
        self.orientation = 'idle'
        self.move_info = {"time": 0, "move": 0}
        self.image = self.getspriteimage()
        self.stamina = 1000
        self.dash_counter = 0
        self.move((config.screen.get_width() / 2, config.screen.get_height() - config.screen.get_height() / 8))
        self.status = {"alive": 1, "dashed": False, "attacking": False, "invulnerable": False}

    def getspriteimage(self):
        """produces a pygame image from the spritesheet"""
        sizex = 22
        sizey = 28
        x = self.move_info["move"] * sizex
        y = orientationLib[self.orientation] * sizey
        return pygame.transform.scale(self.ss.image_at((x, y, sizex, sizey), -1),
                                      (sizex * config.sizer, sizey * config.sizer)).convert_alpha()

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

    def update(self, dt, *args):
        """update Player sprite"""
        if self.status["alive"] > 0:
            # dash or (walk and charge dash)?
            startdash = all((self.js.get_button(js_lib["B"]), self.stamina > 300, self.orientation != "idle",
                             not self.status["dashed"]))
            startattack = all((self.js.get_button(js_lib["A"]), True))  # TODO attack counter instead of True

            if self.dash_counter:
                self.dash(dt)
            elif startdash:
                self.status["dashed"] = True
                self.stamina -= 300
                self.dash(dt)
            elif self.status["attacking"] or startattack:
                self.attack(dt)
            else:
                self.walk(dt)
                if self.stamina < 1000:
                    self.stamina += self.stamina_regen

            if self.status["dashed"] and not self.js.get_button(js_lib["B"]):
                self.status["dashed"] = False

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
            self.hitbox.center = self.rect.center

        elif self.status["alive"] == 0:
            self.orientation = 'death'
            self.death(dt)
