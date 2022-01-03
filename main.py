# Simple pygame program
# Import and initialize the pygame library
import pygame
import time
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN
)

import enemys
from Player import Player
from colorbox import ColorBox
from menus import MainMenu, DeathMenu
import joystick_handler
from game import Game

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

js_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}


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
# TODO make better size multiplier
# laptop 1536x864 -> 1000
# size_multiplier = int((screen.get_width() + screen.get_height()) / 1000)
size_multiplier = 3

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

try:
    # Initialize the joysticks
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
except pygame.error:
    joystick = None
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
        pass

# Done! Time to quit.
pygame.quit()
