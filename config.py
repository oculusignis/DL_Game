import pygame
import game
import spriteSheet
# file that handles global variables for the whole project

screen: pygame.Surface
sheet_button: spriteSheet.SpriteSheet
sheet_player: spriteSheet.SpriteSheet
sizer = 3
framerate = 120
score = 0
difficulty = 0

# main_menu = 10, settings = 11, death_menu = 12, game = 20
# first number is main category, x0 is parent of category
state = 'main_menu'


def init(size=(0, 0)):
    global screen
    screen = pygame.display.set_mode(size)
    global sizer
    global sheet_button
    sheet_button = spriteSheet.SpriteSheet("resources/MenuButtons.png")
    global sheet_player
    sheet_player = spriteSheet.SpriteSheet("resources/Sam66_22-28.png")

    # Todo add all game variables

    '''
    with open('settings.txt') as f:
        for line in f.readlines():
            # execute string as python code
            exec(global '' + line)
    '''


def endit(msg=""):
    pygame.quit()
    if msg:
        print(msg)
    exit()
