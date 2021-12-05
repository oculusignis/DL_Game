import pygame

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)

done = False
while not done:
    pygame.event.get()
    x = joystick.get_button(0)
    print(x)
