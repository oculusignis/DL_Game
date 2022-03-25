import math
import pygame
import config


config.init((600, 600))

clock = pygame.time.Clock()
counter = 0
edge1 = math.pi*1.1
edge2 = math.pi*0.8

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.endit()

    config.screen.fill((20, 180, 180))
    pygame.draw.arc(config.screen, (0, 0, 0), [80, 50, 120, 80], edge1, edge1 + 0.8*math.pi*counter/100)
    pygame.display.flip()
    counter += 2
    counter = counter % 100
    clock.tick(20)
