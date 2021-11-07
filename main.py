# Simple pygame program
# Import and initialize the pygame library
import math
import random
import pygame
from Player import Player
from colorbox import ColorBox
import enemys
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)

# vars
size_multiplier = 3
# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 600
better_black = (39, 41, 50)
light_blue = (198, 211, 232)
light_green = (199, 226, 211)
light_grey = (215, 215, 213)
light_red = (255, 194, 205)
light_violet = (204, 194, 225)
light_yellow = (225, 232, 187)
bg_lib = [light_blue, light_green, light_grey, light_red, light_violet, light_yellow]


# Enemy Class extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("resources/missile.png").convert()
        self.surf.set_colorkey((247, 247, 247), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()

# fullscreen
window_info = pygame.display.Info()
SCREEN_WIDTH = window_info.current_w
SCREEN_HEIGHT = window_info.current_h

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Create custom event for adding new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create Sprite Groups
enemies = pygame.sprite.Group()
boxes = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Instantiate Player
player = Player(size_multiplier)
player.move((SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT/8))
all_sprites.add(player)

# Instantiate Colorbox
randomBox = ColorBox(SCREEN_WIDTH, SCREEN_HEIGHT)
boxes.add(randomBox)
all_sprites.add(randomBox)

# Instantiate Enemy
enemy = enemys.Enemy1(3)
enemies.add(enemy)
all_sprites.add(enemy)

# Setup Clock
clock = pygame.time.Clock()

# setup bg color
bg_color = light_blue

# Run until the user asks to quit
running = True
gaming = False
menu = True
# Window loop
while running:
    # menu loop
    while menu:
        screen.fill(light_grey)
        # TODO Menu Buttons
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = False
                    running = False
                elif event.key == K_SPACE:
                    menu = False
                    gaming = True

        pygame.display.flip()

    # game running loop
    while gaming:

        # Did the user click the window close button?
        for event in pygame.event.get():

            # User press Key?
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gaming = False
                    menu = True

            # User press Close Window?
            elif event.type == QUIT:
                gaming = False

            # Add new enemy?
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == MOUSEBUTTONDOWN:
                player.click = True

        # get set of pressed keys
        pressed_keys = pygame.key.get_pressed()

        # update player
        player.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)

        # update enemies
        enemies.update(player)

        # Check if player has collected a colorbox
        if pygame.sprite.spritecollideany(player, boxes):
            randomBox.move()
            # bg_color = random.choice(bg_lib)
            bg_color = (random.randint(190, 255), random.randint(190, 255), random.randint(190, 255))

        # Set Background Color
        screen.fill(bg_color)

        # Draw all entities
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # Check if any enemies has collided with player
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            player.alive = False
        #     gaming = False

        # Flip the display
        pygame.display.flip()

        # Ensure program maintains 30 FPS
        clock.tick(120)

# Done! Time to quit.
pygame.quit()
