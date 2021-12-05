# Simple pygame program
# Import and initialize the pygame library
import pygame
import random
import time
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)

import enemys
from Player import Player
from colorbox import ColorBox
from menus import MainMenu, DeathMenu

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

joystick_lib = {0: "X", 1: "A", 2: "B", 3: "Y", 4: "LS", 5: "RS", 6: None, 7: None, 8: "Select", 9: "Start"}
joystick_lib2 = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}


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


def game_reset():
    pass


pygame.init()

# fullscreen
window_info = pygame.display.Info()
SCREEN_WIDTH = window_info.current_w
SCREEN_HEIGHT = window_info.current_h
# TODO make it setting
framerate = 120

# Set up the drawing window and name it
# screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption('DL_Game')

# calculate relative to screenw
size_multiplier = int((screen.get_width() + screen.get_height()) / 1000)

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
player = Player(size_multiplier, screen, framerate)
all_sprites.add(player)

# Instantiate Colorbox
randomBox = ColorBox(SCREEN_WIDTH, SCREEN_HEIGHT)
boxes.add(randomBox)
all_sprites.add(randomBox)

# Instantiate Enemy
enemy = enemys.Enemy1(size_multiplier)
enemies.add(enemy)
all_sprites.add(enemy)

# Setup Clock
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Run until the user asks to quit
running = True
game_running = False
menu_running = True
main_menu = MainMenu(screen, size_multiplier)
program_state = "main_menu"

# Window loop
while program_state != "quit":
    # run main_menu loop
    if program_state == "main_menu":
        program_state = main_menu.loop(joystick)

    # run game loop
    if program_state == "game":
        # initiate specific vars
        bg_color = light_blue
        last_time = time.time()

        while program_state == "game":
            # time passed since last frame
            dt = (time.time() - last_time) * framerate
            last_time = time.time()

            # Did the user click the window close button?
            for event in pygame.event.get():
                # User press Key?
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        program_state = "main_menu"
                # User press Close Window?
                elif event.type == QUIT:
                    program_state = "quit"
                # Add new enemy?
                elif event.type == ADDENEMY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

                elif event.type == MOUSEBUTTONDOWN:
                    player.click = True

            # get set of pressed keys
            pressed_keys = pygame.key.get_pressed()

            # get joystick values
            jaxes = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]

            # TODO controller start button to call main_menu

            # update player
            player.update(pressed_keys, joystick, SCREEN_WIDTH, SCREEN_HEIGHT, dt)

            # update enemies
            enemies.update(player, dt)

            # Check if player has collected a colorbox
            if pygame.sprite.spritecollideany(player, boxes):
                randomBox.move()
                # bg_color = random.choice(bg_lib)
                bg_color = (random.randint(170, 250), random.randint(170, 250), random.randint(170, 250))

            # Set Background Color
            screen.fill(bg_color)

            # Draw all entities
            for entity in all_sprites:
                screen.blit(entity.image, entity.rect)

            if player.status["alive"] > 0:
                # Check if any enemies has collided with player
                if pygame.sprite.spritecollideany(player, enemies):
                    player.status["alive"] = 0
                    player.move_info["move"] = 0
            elif player.status["alive"] < 0:
                # player dead -> DeathMenu -> reset game
                dm = DeathMenu((screen, size_multiplier))
                program_state = dm.loop()
                # reset game
                player.reset()
                enemy.reset()
                randomBox.move()

            #     prog_state["game"] = False
            #     prog_state["main_menu"] = True

            if player.status["alive"] < 0:
                pass

            text = f"buttons={jbuttons}     axis={jaxes}"
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, dest=(0, 0))

            # Flip the display
            pygame.display.flip()

            # Ensure program maintains 60 FPS
            clock.tick(framerate)

# Done! Time to quit.
pygame.quit()
