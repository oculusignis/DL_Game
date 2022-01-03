import pygame
import time
from pygame.locals import (QUIT, MOUSEBUTTONDOWN)

import enemys
from Player import Player
from colorbox import ColorBox
from menus import MainMenu, DeathMenu

# variables
bg = (0xeb, 0xd2, 0xbe)
framerate = 120

usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}


class Game:
    def __init__(self, screen, number_of_players):
        self.screen = screen
        self.mult = 3
        # change settings as specified in settings
        with open('settings.txt') as f:
            for line in f.readlines():
                # execute string as python code
                exec("self." + line)

        # Create Sprite Groups and add sprites
        box = ColorBox(self.screen)
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group(enemys.Enemy1(self.mult))
        self.boxes = pygame.sprite.Group(box)
        self.all_sprites = pygame.sprite.Group(box)

        for x in range(number_of_players):
            player = Player(x, self.mult, self.screen, framerate)
            self.players.add(player)
            self.all_sprites.add(player)

    def loop(self):
        # initiate specific vars
        last_time = time.time()
        gaming = True
        clock = pygame.time.Clock()

        while gaming:
            # time stuff
            dt = (time.time() - last_time) * framerate
            last_time = time.time()

            # Did the user click the window close button?
            for event in pygame.event.get():
                # User press Key?
                if event.type == QUIT:
                    return "quit"
                # Add new enemy?
                # elif event.type == ADDENEMY:
                #     new_enemy = Enemy()
                #     enemies.add(new_enemy)
                #     all_sprites.add(new_enemy)

            # mangage player inputs
            for player in self.players:
                if player.js.get_button(usb_lib["Start"]):
                    return "main_menu"

                player.update(dt)

                # update enemies
                self.enemies.update(player, dt)

                # Check if player has collected a colorbox
                if pygame.sprite.spritecollideany(player.sword, self.boxes):
                    print("Transparent hit")

                # player touch box?
                if box := pygame.sprite.spritecollideany(player, self.boxes):
                    box.move()

                # player hit? --> death menu
                if player.status["alive"] > 0:
                    # Check if any enemies has collided with player
                    if pygame.sprite.spritecollideany(player, self.enemies):
                        player.status["alive"] = 0
                        player.move_info["move"] = 0
                elif player.status["alive"] < 0:
                    # player dead -> DeathMenu -> reset game
                    dm = DeathMenu(self.screen, self.mult)
                    program_state = dm.loop(joystick)  # TODO use joystick handler, also in all menus

                    # reset all
                    for entity in self.all_sprites:
                        entity.reset()

            # Set Background Color
            self.screen.fill(bg)

            # Draw all entities
            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            #     prog_state["game"] = False
            #     prog_state["main_menu"] = True

            # Flip the display
            pygame.display.flip()

            # Ensure program maintains 60 FPS
            clock.tick(framerate)
