import pygame


pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
js0 = pygame.joystick.Joystick(0)
js1 = pygame.joystick.Joystick(1)

while True:
    pygame.event.get()
    print(f"js0: {js0.get_button(1)}    js1: {js1.get_button(1)}")
    clock.tick(20)
