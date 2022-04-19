import pygame


class Entity(pygame.sprite.Sprite):
    """Meant for all game objects"""

    def move(self, loc: (int, int)):
        """move character to loc coordinates"""
        self.rect.center = loc


class EntityGroup:

    def __init__(self, *entities: Entity):
        self._entities = list(entities)

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return (e for e in self._entities)

    def add(self, *new_ent):
        for e in new_ent:
            self._entities.append(e)

    def remove(self, *rem_ent):
        for e in rem_ent:
            self._entities.remove(e)


class Character(Entity):
    """movable character in game, with float"""
    def __int__(self):
        self.hitbox = pygame.rect.Rect(0, 0, 1, 1)
        self.pos = pygame.Vector2(0, 0)

    def move(self, loc: (int, int)):
        """move character to loc coordinates"""
        self.pos.update(loc)
        self.rect.center = loc

    def reset(self):
        self.move((0, 0))


class CharacterGroup(EntityGroup):
    """Group of _characters, for collective activities"""

    def __init__(self, *characters: Character):
        self._characters = list(characters)

    def __len__(self):
        return len(self._characters)

    def __iter__(self):
        return (c for c in self._characters)

    def add(self, *new_characters):
        for c in new_characters:
            self._characters.append(c)

    def remove(self, *rem_characters):
        for c in rem_characters:
            self._characters.remove(c)

    def has(self, character):
        return character in self._characters

    def update(self):
        for c in self._characters:
            c.update()

    def draw(self, surface: pygame.Surface):
        for c in self._characters:
            surface.blit(c.image, c.rect)


def collisions(entity: Entity, group: EntityGroup):
    pass
