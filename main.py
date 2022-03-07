# Simple pygame program
# Import and initialize the pygame library
import pygame
import config

import enemys
from Player import Player
from colorbox import ColorBox
import menus
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

# Setup Clock
clock = pygame.time.Clock()
config.init()

# Run until the user asks to quit
main_menu = menus.MainMenu()
setting_menu = menus.SettingsMenu()
death_menu = menus.DeathMenu()
game = Game(1)

# Window loop
while config.state != "quit":
    # run main_menu loop
    if config.state == "main_menu":
        program_state = main_menu.loop()
    # run game loop
    elif config.state == "game":
        game.loop()
    # go in settings
    elif config.state == "settings":
        setting_menu.loop()
    # call menu of shame
    elif config.state == "death_menu":
        death_menu.loop()
        game.reset()

# Done! Time to quit.
pygame.quit()
