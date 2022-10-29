import pygame
import time
import math
import random
import my_creations
from pygame.locals import QUIT

framerate = 60
usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}
bg = (0xfd, 0xf4, 0xe3)

pygame.init()
pygame.joystick.init()

# fullscreen
window_info = pygame.display.Info()
SCREEN_WIDTH = window_info.current_w
SCREEN_HEIGHT = window_info.current_h

# Set up the drawing window and name it
# screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption('CLEAN')
pygame.mouse.set_visible(False)

# initiate specific vars
last_time = time.time()
clock = pygame.time.Clock()

# TODO remove/improve
js = pygame.joystick.Joystick(0)
js.init()
if js.get_name == "usb gamepad":
    js_lib = usb_lib
else:
    # TODO
    js_lib = usb_lib


simple = my_creations.Basic()


print(f"js_id: {js.get_instance_id()}, js_name: {js.get_name()}")

done = False
while not done:
    dt = (time.time() - last_time) * framerate
    last_time = time.time()

    # OS says close game
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            js_press = True
            # manage user input
            if js.get_button(js_lib['Start']):
                done = True
            elif js.get_button(js_lib['A']):
                bg = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # ------------------------------------------
    # test code
    # ------------------------------------------
    dpad = pygame.math.Vector2(round(js.get_axis(0)), round(js.get_axis(1)))
    simple.update(dpad)

    screen.fill(bg)
    screen.blit(simple.image, simple.rect)
    pygame.display.flip()

pygame.quit()
