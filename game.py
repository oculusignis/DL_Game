import pygame
import time
import math
from pygame.locals import QUIT
import config
import enemys

# TODO implement mcreations
import mcreations

# variables
bg = (0xeb, 0xd2, 0xbe)
edge1 = 1.1 * math.pi

usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}


class Game:
    def __init__(self, number_of_players):
        # Create Sprite Groups and add sprites
        box = mcreations.ColorBox()
        self.players = mcreations.EntityGroup()
        test_enemy = enemys.Enemy1()
        self.enemies = mcreations.EntityGroup(test_enemy)
        self.boxes = mcreations.EntityGroup(box)
        self.all_sprites = mcreations.EntityGroup(box, test_enemy)

        for x in range(number_of_players):
            player = mcreations.Player(x)
            self.players.add(player)
            self.all_sprites.add(player)

    def reset(self):
        self.all_sprites.reset()
        config.difficulty = 0

    def loop(self):
        # initiate specific vars
        last_time = time.time()
        gaming = True
        clock = pygame.time.Clock()
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        screenw = config.screen.get_width()
        screenh = config.screen.get_height()
        p_num = len(self.players)

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

                # player touch box?
                if boxes := mcreations.collisions(player, self.boxes):
                    for box in boxes:
                        box.move("random")
                        player.score += 1
                        config.difficulty += 1

                # player hit? --> death menu
                if player.status["alive"] > 0:
                    # Check if any enemies has collided with player
                    if mcreations.collisions(player, self.enemies):
                        player.status["alive"] = 0
                        player.move_info["move"] = 0
                elif player.status["alive"] < 0:
                    # update highscore
                    if config.sdata["highscore"] < config.difficulty:
                        config.sdata["highscore"] = config.difficulty
                    # player dead -> DeathMenu -> reset game
                    config.state = "death_menu"
                    return

            # update enemies
            self.enemies.update(dt, self.players)

            # Set Background Color
            config.screen.fill(bg)

            # Draw all entities
            self.all_sprites.draw(config.screen)

            # TODO fix drawing
            # draw stamina and score

            for num, player in enumerate(self.players, 1):
                color = (80, 80, 80) if player.stamina == 1000 else (150, 150, 150)
                a = player.rect.left + 4 * config.sizer
                b = player.rect.bottom
                c = player.rect.width - 8 * config.sizer
                d = 5 * config.sizer
                for i in range(3):
                    pygame.draw.arc(config.screen, color, [a, b + i, c, d], edge1,
                                    edge1 + 0.8 * math.pi * float(player.stamina) / 1000)
                    # TODO remove following
                    # st_surf = font.render(str(player.stamina), True, (0, 0, 0))
                    # config.screen.blit(st_surf, dest=(screenw/2, 50))

                score_string = ";)" if config.score == 69 else str(player.score)
                text_surface = font.render(score_string, True, (0, 0, 0))
                config.screen.blit(text_surface, dest=(num * screenw / (p_num+1), 10))


            # Draw Score
            # score_string = ";)" if config.score == 69 else str(config.score)
            # text_surface = font.render(score_string, True, (0, 0, 0))
            # config.screen.blit(text_surface, dest=(screenw/2, 10))

            #     prog_state["game"] = False
            #     prog_state["main_menu"] = True

            # Flip the display
            pygame.display.flip()

            # Ensure program maintains 60 FPS
            clock.tick(config.framerate)
