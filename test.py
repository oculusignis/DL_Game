import math
import pygame
import config
import enemys


def arctest():
    edge1 = math.pi * 1.1
    edge2 = math.pi * 0.8
    clock = pygame.time.Clock()
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.endit()

        config.screen.fill((20, 180, 180))
        for i in range(3):
            pygame.draw.arc(config.screen, (0, 0, 0), [80, 50 - i, 120, 80], edge1,
                            edge1 + 0.8 * math.pi * counter / 100)
        pygame.display.flip()
        counter += 2
        counter = counter % 100
        clock.tick(20)


def imagetest():
    clock = pygame.time.Clock()
    en = enemys.Enemy1()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.endit()

        config.screen.fill((20, 180, 180))

        en.move(pygame.mouse.get_pos())
        config.screen.blit(en.image, en.rect)

        pygame.display.flip()
        clock.tick(20)


config.init((600, 600))
imagetest()



