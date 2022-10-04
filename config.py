import pygame
import spriteSheet
import json
# file that handles global variables for the whole project

screen: pygame.Surface
sheet_button: spriteSheet.SpriteSheet
sheet_player: spriteSheet.SpriteSheet
sizer = 2
framerate = 120
score = 0
difficulty = 0
font: pygame.font.Font

sdata = {}


# TODO library with startpositions for x players
start_pos = {1: (1/2, )}

# main_menu = 10, settings = 11, death_menu = 12, game = 20
# first number is main category, x0 is parent of category
state = 'main_menu'


def init(size=(0, 0)):
    global screen
    global sdata
    global sizer
    global framerate
    sdata = jread()
    sizer = sdata["sizer"]
    framerate = sdata["framerate"]

    screen = pygame.display.set_mode(size)
    global sheet_button
    sheet_button = spriteSheet.SpriteSheet("resources/MenuButtons.png")
    global sheet_player
    sheet_player = spriteSheet.SpriteSheet("resources/Sam66_22-28.png")
    global font
    font = pygame.font.Font(pygame.font.get_default_font(), 36)

    # Todo add all game variables


def endit(msg=""):
    pygame.quit()
    save(sdata)
    if msg:
        print(msg)
    exit()


def save(dt: dict):
    json_object = json.dumps(dt, indent=len(dt))
    with open("config.json", "w") as file:
        file.write(json_object)


def jread():
    with open("config.json", "r") as file:
        loaded = json.load(file)
        return loaded


# use this to reset the config.json file
if __name__ == "__main__":
    resetdict = {"sizer": 3,
                 "framerate": 120,
                 "highscore": 0
                 }
    save(resetdict)
