import pygame
import numpy as np
import spriteSheet
from pygame.locals import (K_a, K_d, K_ESCAPE, K_SPACE, KEYDOWN, QUIT)


class Menu:
    """manages menu_running buttons and their states"""
    def __init__(self, screen, sizer: int):
        self.active = 0
        self.states = {0: "play", 1: "settings", 2: "exit"}
        window_stats = (screen.get_width(), screen.get_height(), sizer)
        play_button = MenuButton(0, 1, window_stats)
        setting_button = MenuButton(1, 0, window_stats)
        exit_button = MenuButton(2, 0, window_stats)
        self.buttons = (play_button, setting_button, exit_button)
        self.screen = screen
        self.settings = SettingsMenu(screen, window_stats)

    def update(self, events):
        """update Buttons"""
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.active = (self.active - 1) % 3
                if event.key == K_d:
                    self.active = (self.active + 1) % 3

        for button in self.buttons:
            button.update(self.active)

    def loop(self, program_state):
        """runs the menu"""
        menu_color = (0xeb, 0xd2, 0xbe)
        while True:
            self.screen.fill(menu_color)

            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "quit"
                    if event.key == K_SPACE:
                        if self.states[self.active] == "play":
                            return "game"
                        elif self.states[self.active] == "settings":
                            self.settings.loop()
                        elif self.states[self.active] == "exit":
                            return "quit"
                            return
                elif event.type == QUIT:
                    return "quit"

            self.update(events)
            for button in self.buttons:
                self.screen.blit(button.image, button.rect)
            pygame.display.flip()


class MenuButton(pygame.sprite.Sprite):
    """Sprite and state of a menu_running button"""

    def __init__(self, button_number, highlight, window_stats):
        super(MenuButton, self).__init__()
        screenw, screenh, self.size_multiplier = window_stats
        self.b_number = button_number
        self.highlight = highlight
        self.ss = spriteSheet.SpriteSheet("resources/MenuButtons.png")
        self.image = pygame.transform.scale(self.ss.image_at((button_number * 56, highlight * 40, 56, 40), -1),
                                            (56 * self.size_multiplier, 40 * self.size_multiplier))
        self.rect = self.image.get_rect(
            center=((button_number+3) * screenw / 8, screenh*3/5)
        )

    def update(self, active, *args, **kwargs) -> None:
        """update highlight stat, if changed update image"""
        new_state = 1 if active == self.b_number else 0
        if self.highlight != new_state:
            self.highlight = new_state
            self.image = pygame.transform.scale(self.ss.image_at((self.b_number * 56, self.highlight * 40, 56, 40), -1),
                                                (56 * self.size_multiplier, 40 * self.size_multiplier))


class SettingsMenu:
    def __init__(self, screen: pygame.display, window_stats):
        self.screen = screen
        self.visionB = SettingsButton(0, 1, window_stats)
        self.buttons = [self.visionB]
        self.active = self.visionB

    def loop(self):
        """runs the menu"""
        menu_color = (0xeb, 0xd2, 0xbe)
        while True:
            self.screen.fill(menu_color)

            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_SPACE:
                        self.active.update(1)
                    if event.key == K_d:
                        self.active.update(1)
                    if event.key == K_a:
                        self.active.update(-1)
                    elif event.type == QUIT:
                        return

            for button in self.buttons:
                self.screen.blit(button.image, button.rect)
            pygame.display.flip()


class SettingsButton(pygame.sprite.Sprite):
    """Sprite and state of a Settings Button"""

    def __init__(self, button_number, highlight, window_stats):
        super(SettingsButton, self).__init__()
        screenw, screenh, self.size_multiplier = window_stats
        self.size_multiplied = (32 * self.size_multiplier, 32 * self.size_multiplier)
        self.b_number = button_number
        self.highlight = highlight
        self.setting = 0
        self.ss = spriteSheet.SpriteSheet("resources/MenuButtons.png")
        self.image = pygame.transform.scale(self.ss.image_at((self.setting * 32, 80 + highlight * 32, 32, 32), -1),
                                            self.size_multiplied)
        self.rect = self.image.get_rect(
            center=(50, 50)  # TODO relative coordinates
        )

    def update(self, increment):
        self.setting = (self.setting + increment) % 2
        self.image = pygame.transform.scale(self.ss.image_at((self.setting * 32, 80 + self.highlight * 32, 32, 32), -1),
                                            self.size_multiplied)


# TODO show menu on some kind of surface or display
# TODO loop function
# TODO change code in main
class DeathMenu:
    """menu shown when player dies"""
    def __init__(self, window_stats: (pygame.display, int)):
        self.screen, self.sizer = window_stats
        self.test, x = window_stats
        self.playB = DeathButton(0, True, window_stats)
        self.homeB = DeathButton(3, False, window_stats)

    def get_background(self):
        """returns old game state with opaque layers on top as a Surface"""
        # copy of game_screen for menu background
        old_game = self.screen.copy()
        center = old_game.get_rect().center
        width, height = old_game.get_size()
        opaque_surf = pygame.Surface(old_game.get_size()).convert_alpha()
        opaque_surf.set_alpha(20)
        opaque_surf.fill((40, 40, 40))
        # put decreasing sized opaque layers on old_game
        for rel_width in np.linspace(1, 0.3, 5):
            opaque_surf = pygame.transform.scale(opaque_surf, (int(width * rel_width), height)).convert_alpha()
            opaque_rect = opaque_surf.get_rect(center=center)
            old_game.blit(opaque_surf, opaque_rect)
        return old_game

    def loop(self):
        bg = self.get_background()
        bg_rect = bg.get_rect()

        while True:
            # handle events
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "menu"
                    if event.key == K_a or event.key == K_d:
                        self.playB.update()
                        self.homeB.update()
                    if event.key == K_SPACE:
                        if self.playB.highlight:
                            return "game"
                        else:
                            return "menu"
                # quitting the program
                elif event.type == QUIT:
                    return "quit"

            # show game behind tranpsarent surface
            self.screen.blit(bg, bg_rect)
            # show buttons
            self.screen.blit(self.playB.image, self.playB.rect)
            self.screen.blit(self.homeB.image, self.homeB.rect)

            # TODO death buttons, sprite and function
            pygame.display.flip()


# TODO update funtion
class DeathButton(pygame.sprite.Sprite):
    """Sprite and state of death menu button"""
    def __init__(self, button_number, highlight, window_stats):
        super(DeathButton, self).__init__()
        self.bn = button_number
        screen, self.size_multiplier = window_stats
        self.highlight = highlight
        self.ss = spriteSheet.SpriteSheet("resources/MenuButtons.png")
        self.image = pygame.transform.scale(self.ss.image_at((button_number * 56, highlight * 40, 56, 40), -1),
                                            (56 * self.size_multiplier, 40 * self.size_multiplier))
        offset = int(screen.get_width()/16) if button_number > 0 else -int(screen.get_width()/16)
        self.rect = self.image.get_rect(center=(screen.get_width()/2 + offset, screen.get_height() * 3/5))
        self.color = (0, 255, 0) if button_number > 0 else (255, 0, 0)

    def update(self):
        """toggle highlight on button on/off"""
        self.highlight = not self.highlight
        self.image = pygame.transform.scale(self.ss.image_at((self.bn * 56, self.highlight * 40, 56, 40), -1),
                                            (56 * self.size_multiplier, 40 * self.size_multiplier))
