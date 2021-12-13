import pygame
import numpy as np
import spriteSheet
from pygame.locals import (K_a, K_d, K_s, K_w, K_ESCAPE, K_SPACE, KEYDOWN, QUIT)
import time

js_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}

clock = pygame.time.Clock()


class MainMenu:
    """manages menu_running buttons and their states"""
    def __init__(self, screen: pygame.Surface, sizer: int):
        self.active = 0
        self.states = {0: "play", 1: "settings", 2: "exit"}
        window_stats = (screen.get_width(), screen.get_height(), sizer)
        self.ss = spriteSheet.SpriteSheet("resources/MenuButtons.png")
        play_button = MainButton(0, 1, window_stats, self.ss)
        setting_button = MainButton(1, 0, window_stats, self.ss)
        exit_button = MainButton(2, 0, window_stats, self.ss)
        self.buttons = (play_button, setting_button, exit_button)
        self.screen = screen
        self.settings = SettingsMenu(screen, sizer, self.ss)
        self.axis = 0

    def update(self, events, joystick):
        """update Buttons"""

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.active = (self.active - 1) % 3
                if event.key == K_d:
                    self.active = (self.active + 1) % 3

        axis = round(joystick.get_axis(0))
        if self.axis != axis:
            self.axis = axis
            self.active = (self.active + axis) % 3

        for button in self.buttons:
            button.update(self.active)

    def loop(self, joystick: pygame.joystick.Joystick):
        """runs the main_menu"""
        menu_color = (0xeb, 0xd2, 0xbe)
        # first draw
        self.screen.fill(menu_color)
        for button in self.buttons:
            self.screen.blit(button.image, button.rect)
        pygame.display.flip()
        # wait for user to stop pressing start
        while joystick.get_button(js_lib["Start"]):
            pygame.event.get()
            clock.tick(20)
        # start menu loop
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
                            if self.settings.loop(joystick) == "quit":
                                return "quit"
                        elif self.states[self.active] == "exit":
                            return "quit"
                elif event.type == QUIT:
                    return "quit"

            # get joystick values
            jaxes = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]

            if jbuttons[js_lib["A"]] or jbuttons[js_lib["Select"]]:
                if self.states[self.active] == "play":
                    return "game"
                elif self.states[self.active] == "settings":
                    if self.settings.loop(joystick) == "quit":
                        return "quit"
                elif self.states[self.active] == "exit":
                    return "quit"

            if jbuttons[js_lib["Start"]]:
                return "game"

            self.update(events, joystick)
            for button in self.buttons:
                self.screen.blit(button.image, button.rect)
            pygame.display.flip()
            clock.tick(120)


class MainButton(pygame.sprite.Sprite):
    """Sprite and state of a menu_running button"""

    def __init__(self, button_number, highlight, window_stats, ss: spriteSheet.SpriteSheet):
        super(MainButton, self).__init__()
        screenw, screenh, self.size_multiplier = window_stats
        self.b_number = button_number
        self.highlight = highlight
        self.ss = ss
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
    def __init__(self, screen: pygame.Surface, sizer, ss: spriteSheet.SpriteSheet):
        # variables
        self.screen = screen
        self.screenw = screen.get_width()
        self.screenh = screen.get_height()
        self.sizer = sizer
        self.axis = 0
        # init buttons
        self.visionB = SettingButton(0, 1, self.screenw, self.screenh, self.sizer, ss)
        self.enemyB = SettingButton(1, 0, self.screenw, self.screenh, self.sizer, ss)
        self.cB = SettingButton(2, 0, self.screenw, self.screenh, self.sizer, ss)
        self.dB = SettingButton(3, 0, self.screenw, self.screenh, self.sizer, ss)
        self.buttons = [self.visionB, self.enemyB, self.cB, self.dB]
        self.active = self.visionB
        # settings bar
        self.bg = self.screen.copy()
        self.bg.fill((0xeb, 0xd2, 0xbe))
        bar_dim = (int(self.screenw/4), sizer*8)
        bar = pygame.transform.scale(ss.image_at((136, 88, 8, 8), (255, 255, 255)), bar_dim)
        spot = pygame.transform.scale(ss.image_at((152, 88, 10, 10), -1), (sizer*10, sizer*10))
        for i in range(4):
            bar_rect = bar.get_rect(center=(self.screenw/2, (3+i)/8*self.screenh))
            self.bg.blit(bar, bar_rect)
            for k in range(3):
                spotr = spot.get_rect(center=((3+k)/8 * self.screenw, (3+i)/8*self.screenh))
                self.bg.blit(spot, spotr)

    def loop(self, joystick: pygame.joystick.Joystick):
        """runs the main_menu"""
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        # first drawing
        self.screen.blit(self.bg, self.bg.get_rect())
        for button in self.buttons:
            self.screen.blit(button.image, button.rect)
        pygame.display.flip()
        # while "A" is still pressed do nothing
        while joystick.get_button(js_lib["A"]):
            pygame.event.get()
            clock.tick(30)
        old_axes = [0, 0]
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "main_menu"
                    if event.key == K_SPACE:
                        self.active.update(1)
                    if event.key == K_d:
                        self.active.update(1)
                    if event.key == K_a:
                        self.active.update(-1)
                    if event.key == K_s:
                        self.active.toggle()
                        self.active = self.buttons[(self.buttons.index(self.active) + 1) % 4]
                        self.active.toggle()
                    if event.key == K_w:
                        self.active.toggle()
                        self.active = self.buttons[(self.buttons.index(self.active) - 1) % 4]
                        self.active.toggle()
                    elif event.type == QUIT:
                        return
                if event.type == QUIT:
                    return "quit"

            # get joystick values
            horizontal, vertical = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]

            if jbuttons[js_lib["Start"]] or jbuttons[js_lib["Y"]]:
                while joystick.get_button(js_lib["Start"]):
                    pygame.event.get()
                    clock.tick(20)
                return "main_menu"

            if horizontal and horizontal != old_axes[0]:
                self.active.update(horizontal)
            if vertical and vertical != old_axes[1]:
                self.active.toggle()
                self.active = self.buttons[(self.buttons.index(self.active) + vertical) % 4]
                self.active.toggle()

            # update old_axes
            old_axes = [horizontal, vertical]

            self.screen.blit(self.bg, self.bg.get_rect())
            for button in self.buttons:
                self.screen.blit(button.image, button.rect)

            # now print the text
            text = f"buttons={jbuttons}     axis={[horizontal, vertical]}       oldaxes={old_axes}"
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, dest=(0, 0))

            pygame.display.flip()
            clock.tick(120)


class SettingButton(pygame.sprite.Sprite):
    """Sprite and state of a Settings Button"""

    def __init__(self, button_number, highlight, screenw, screenh, sizer, ss: spriteSheet.SpriteSheet):
        super(SettingButton, self).__init__()
        self.screenw = screenw
        self.screenh = screenh
        self.sizer = sizer
        self.ss = ss
        self.size_multiplied = (32 * self.sizer, 32 * self.sizer)
        self.b_number = button_number
        self.highlight = highlight
        self.setting = 0
        self.image = pygame.transform.scale(self.ss.image_at((self.b_number*32, 80+highlight*32, 32, 32), -1),
                                            self.size_multiplied)
        self.rect = self.image.get_rect(center=((3 + self.setting)/8*screenw, (3 + button_number)/8*screenh))

    def update(self, increment):
        """Setting is changed based on increment"""
        self.setting = (self.setting + increment)
        if self.setting < 0:
            self.setting = 0
        elif self.setting > 2:
            self.setting = 2
        self.rect = self.image.get_rect(center=((3 + self.setting)/8*self.screenw, (3 + self.b_number)/8*self.screenh))

    def toggle(self):
        """toggle the highlight on the button"""
        self.highlight = (self.highlight + 1) % 2
        self.image = pygame.transform.scale(self.ss.image_at((self.b_number*32, 80+self.highlight*32, 32, 32), -1),
                                            self.size_multiplied)


class DeathMenu:
    """main_menu shown when player dies"""
    def __init__(self, window_stats: (pygame.Surface, int)):
        self.screen, self.sizer = window_stats
        self.test, x = window_stats
        self.playB = DeathButton(0, True, window_stats)
        self.homeB = DeathButton(3, False, window_stats)

    def get_background(self):
        """returns old game state with opaque layers on top as a Surface"""
        # copy of game_screen for main_menu background
        old_game = self.screen.copy()
        center = old_game.get_rect().center
        width, height = old_game.get_size()
        # opaque surface preparation
        opaque_surf = pygame.Surface(old_game.get_size()).convert_alpha()
        opaque_surf.set_alpha(1)
        opaque_surf.fill((40, 40, 40))
        # put decreasing sized opaque layers on old_game
        for rel_width in np.linspace(0.3, 0.8, 40):
            opaque_surf = pygame.transform.scale(opaque_surf, (int(width * rel_width), height))
            opaque_rect = opaque_surf.get_rect(center=center)
            old_game.blit(opaque_surf, opaque_rect)
        return old_game

    def loop(self):
        joystick = pygame.joystick.Joystick(0)

        # draw death menu for the first time
        bg = self.get_background()
        bg_rect = bg.get_rect()
        self.screen.blit(bg, bg_rect)
        self.screen.blit(self.playB.image, self.playB.rect)
        self.screen.blit(self.homeB.image, self.homeB.rect)
        pygame.display.flip()

        # run death menu loop
        while True:
            # handle events
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "main_menu"
                    if event.key == K_a or event.key == K_d:
                        self.playB.update()
                        self.homeB.update()
                    if event.key == K_SPACE:
                        if self.playB.highlight:
                            return "game"
                        else:
                            return "main_menu"
                # quitting the program
                elif event.type == QUIT:
                    return "quit"

            # get joystick values
            horizontal, vertical = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]

            if jbuttons[js_lib["Y"]]:
                return "main_menu"
            if jbuttons[js_lib["Start"]]:
                while joystick.get_button(js_lib["Start"]):
                    pygame.event.get()
                    clock.tick(30)
                return "game"
            if horizontal:
                self.playB.update()
                self.homeB.update()
                # show buttons
                self.screen.blit(self.playB.image, self.playB.rect)
                self.screen.blit(self.homeB.image, self.homeB.rect)

                pygame.display.flip()
                while round(joystick.get_axis(0)):
                    pygame.event.get()
                    clock.tick(30)
            if jbuttons[js_lib["A"]]:
                while joystick.get_button(js_lib["A"]):
                    pygame.event.get()
                    clock.tick(30)
                if self.playB.highlight:
                    return "game"
                else:
                    return "main_menu"

            clock.tick(120)


class DeathButton(pygame.sprite.Sprite):
    """Sprite and state of death main_menu button"""
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
