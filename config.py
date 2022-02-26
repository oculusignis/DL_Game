import pygame
# file that handles global variables for the whole project

screen: pygame.Surface
sizer = 1
state = 11   # main_menu = 10, settings = 11, game = 20     first number is main category, x0 is parent of category


def __init__(size=(0, 0)):
    global screen
    screen = pygame.display.set_mode(size)
    global sizer
    # Todo add all game variables

    '''
    with open('settings.txt') as f:
        for line in f.readlines():
            # execute string as python code
            exec(global '' + line)
    '''
