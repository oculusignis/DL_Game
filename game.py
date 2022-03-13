import pygame
import time
from pygame.locals import QUIT
import config
import enemys
from Player import Player
from colorbox import ColorBox

# variables
bg = (0xeb, 0xd2, 0xbe)

usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}


class Game:
    def __init__(self, number_of_players):
        # Create Sprite Groups and add sprites
        box = ColorBox()
        self.players = pygame.sprite.Group()
        test_enemy = enemys.Enemy1()
        self.enemies = pygame.sprite.Group(test_enemy)
        self.boxes = pygame.sprite.Group(box)
        self.all_sprites = pygame.sprite.Group(box, test_enemy)

        for x in range(number_of_players):
            player = Player(x)
            self.players.add(player)
            self.all_sprites.add(player)

    def reset(self):
        for entity in self.all_sprites:
            entity.reset()
        config.score = 0

    def loop(self):
        # initiate specific vars
        last_time = time.time()
        gaming = True
        clock = pygame.time.Clock()
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        screenw = config.screen.get_width()
        screenh = config.screen.get_height()

        while gaming:
            # time stuff
            dt = (time.time() - last_time) * config.framerate
            last_time = time.time()

            # Did the user click the window close button?
            for event in pygame.event.get():
                # User press Key?
                if event.type == QUIT:
                    config.endit()
                # Add new enemy?
                # elif event.type == ADDENEMY:
                #     new_enemy = Enemy()
                #     enemies.add(new_enemy)
                #     all_sprites.add(new_enemy)

            # mangage player inputs
            for player in self.players:
                if player.js.get_button(usb_lib["Start"]):
                    config.state = "main_menu"
                    return

                player.update(dt)

                # update enemies
                self.enemies.update(player, dt)

                # Check if player has collected a colorbox
                # if pygame.sprite.spritecollideany(player.sword, self.boxes):
                #     print("Transparent hit")

                # player touch box?
                if box := pygame.sprite.spritecollideany(player, self.boxes):
                    box.move()
                    config.score += 1

                # player hit? --> death menu
                if player.status["alive"] > 0:
                    # Check if any enemies has collided with player
                    if pygame.sprite.spritecollideany(player, self.enemies):
                        player.status["alive"] = 0
                        player.move_info["move"] = 0
                elif player.status["alive"] < 0:
                    # player dead -> DeathMenu -> reset game
                    config.state = "death_menu"
                    return

            # Set Background Color
            config.screen.fill(bg)

            # Draw all entities
            for entity in self.all_sprites:
                config.screen.blit(entity.image, entity.rect)

            # Draw Score
            text_surface = font.render(str(config.score), True, (0, 0, 0))
            config.screen.blit(text_surface, dest=(screenw/2, 10))

            #     prog_state["game"] = False
            #     prog_state["main_menu"] = True

            # Flip the display
            pygame.display.flip()

            # Ensure program maintains 60 FPS
            clock.tick(config.framerate)


