import pygame
import numpy as np
import config
import joystick_handler
import spriteSheet
from pygame.locals import (QUIT)

js_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}

clock = pygame.time.Clock()


class MainMenu:
    """manages buttons and their states"""
    def __init__(self):
        self.active = 0
        self.states = {0: "play", 1: "settings", 2: "exit"}
        ss = config.sheet_button
        play_button = MainButton(0, 1, ss)
        setting_button = MainButton(1, 0, ss)
        exit_button = MainButton(2, 0, ss)
        self.buttons = (play_button, setting_button, exit_button)
        self.settings = SettingsMenu()
        self.axis = 0

    def update(self):
        """update Buttons"""

        # get joystick
        try:
            joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            joystick_handler.js_nocontroller()
            joystick = pygame.joystick.Joystick(0)

        axis = round(joystick.get_axis(0))
        if self.axis != axis:
            self.axis = axis
            self.active = (self.active + axis) % 3

        for button in self.buttons:
            button.update(self.active)

    def loop(self):
        """runs the main_menu"""
        menu_color = (0xeb, 0xd2, 0xbe)

        # get joystick
        try:
            joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            joystick_handler.js_nocontroller()
            joystick = pygame.joystick.Joystick(0)

        # first draw
        config.screen.fill(menu_color)
        for button in self.buttons:
            config.screen.blit(button.image, button.rect)
        pygame.display.flip()

        # wait for user to stop pressing start
        while joystick.get_button(js_lib["Start"]):
            pygame.event.get()
            clock.tick(20)
        # start menu loop
        while config.state == "main_menu":
            config.screen.fill(menu_color)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    config.endit()

            # get js values
            jbuttons = [joystick.get_button(b) for b in range(10)]

# Todo manage states below
            if jbuttons[js_lib["A"]] or jbuttons[js_lib["Select"]]:
                if self.states[self.active] == "play":
                    config.state = "game"
                    return
                elif self.states[self.active] == "settings":
                    self.settings.loop()
                elif self.states[self.active] == "exit":
                    config.endit()

            if jbuttons[js_lib["Start"]]:
                config.state = "game"
                return

            self.update()
            for button in self.buttons:
                config.screen.blit(button.image, button.rect)
            pygame.display.flip()
            clock.tick(120)


class MainButton(pygame.sprite.Sprite):
    """Sprite and state of a menu_running button"""

    def __init__(self, button_number, highlight, ss: spriteSheet.SpriteSheet):
        super(MainButton, self).__init__()
        self.b_number = button_number
        self.highlight = highlight
        self.ss = ss
        self.image = pygame.transform.scale(self.ss.image_at((button_number * 56, highlight * 40, 56, 40), -1),
                                            (56 * config.sizer, 40 * config.sizer))
        self.rect = self.image.get_rect(
            center=((button_number+3) * config.screen.get_width() / 8, config.screen.get_height() * 3/5)
        )

    def update(self, active, *args, **kwargs) -> None:
        """update highlight stat, if changed update image"""
        new_state = 1 if active == self.b_number else 0
        if self.highlight != new_state:
            self.highlight = new_state
            self.image = pygame.transform.scale(self.ss.image_at((self.b_number * 56, self.highlight * 40, 56, 40), -1),
                                                (56 * config.sizer, 40 * config.sizer))


class SettingsMenu:
    def __init__(self):
        # variables
        ss = config.sheet_button
        screenw = config.screen.get_width()
        screenh = config.screen.get_height()
        self.axis = 0
        # init buttons
        self.visionB = SettingButton(0, 1, screenw, screenh, config.sizer, ss)
        self.enemyB = SettingButton(1, 0, screenw, screenh, config.sizer, ss)
        self.cB = SettingButton(2, 0, screenw, screenh, config.sizer, ss)
        self.dB = SettingButton(3, 0, screenw, screenh, config.sizer, ss)
        self.buttons = [self.visionB, self.enemyB, self.cB, self.dB]
        self.active = self.visionB
        # settings bar
        self.bg = config.screen.copy()
        self.bg.fill((0xeb, 0xd2, 0xbe))
        bar_dim = (int(screenw/4), config.sizer*8)
        bar = pygame.transform.scale(ss.image_at((136, 88, 8, 8), (255, 255, 255)), bar_dim)
        spot = pygame.transform.scale(ss.image_at((152, 88, 10, 10), -1), (config.sizer*10, config.sizer*10))
        for i in range(4):
            bar_rect = bar.get_rect(center=(screenw/2, (3+i) / 8*screenh))
            self.bg.blit(bar, bar_rect)
            for k in range(3):
                spotr = spot.get_rect(center=((3+k)/8 * screenw, (3+i) / 8*screenh))
                self.bg.blit(spot, spotr)

    def loop(self):
        """runs the main_menu"""
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        # first drawing
        config.screen.blit(self.bg, self.bg.get_rect())
        for button in self.buttons:
            config.screen.blit(button.image, button.rect)
        pygame.display.flip()

        joystick = pygame.joystick.Joystick(0)
        if joystick:
            # while "A" is still pressed do nothing
            while joystick.get_button(js_lib["A"]):
                pygame.event.get()
                clock.tick(30)
        old_axes = [0, 0]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    config.endit()

            # get js values
            horizontal, vertical = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]
            text = f"buttons={jbuttons}     axis={[horizontal, vertical]}       oldaxes={old_axes}"

            if any((jbuttons[js_lib["Start"]], jbuttons[js_lib["B"]])):
                # while any((joystick.get_button(js_lib["Start"]), joystick.get_button(js_lib["B"]))):
                #     pygame.event.get()
                #     clock.tick(20)
                config.state = "main_menu"
                return

            if horizontal and horizontal != old_axes[0]:
                self.active.update(horizontal)
            if vertical and vertical != old_axes[1]:
                self.active.toggle()
                self.active = self.buttons[(self.buttons.index(self.active) + vertical) % 4]
                self.active.toggle()

            # update old_axes
            old_axes = [horizontal, vertical]

            config.screen.blit(self.bg, self.bg.get_rect())
            for button in self.buttons:
                config.screen.blit(button.image, button.rect)

            # now print the text
            text_surface = font.render(text, True, (0, 0, 0))
            config.screen.blit(text_surface, dest=(0, 0))

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
    def __init__(self):
        self.playB = DeathButton(0, True)
        self.homeB = DeathButton(3, False)

    def get_background(self):
        """returns old game state with opaque layers on top as a Surface"""
        # copy of game_screen for main_menu background
        old_game = config.screen.copy()
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
        """displays and controlls the deathmenu, sets future program state before returning"""
        # draw death menu for the first time
        bg = self.get_background()
        bg_rect = bg.get_rect()
        config.screen.blit(bg, bg_rect)
        config.screen.blit(self.playB.image, self.playB.rect)
        config.screen.blit(self.homeB.image, self.homeB.rect)
        pygame.display.flip()

        joystick = pygame.joystick.Joystick(0)

        # run death menu loop
        while True:
            # handle events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    config.endit()

            # get js values
            horizontal, vertical = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            jbuttons = [joystick.get_button(b) for b in range(10)]

            if jbuttons[js_lib["Y"]]:
                config.state = "main_menu"
                return
            if jbuttons[js_lib["Start"]]:
                while joystick.get_button(js_lib["Start"]):
                    pygame.event.get()
                    clock.tick(30)
                config.state = "game"
                return
            if horizontal:
                self.playB.update()
                self.homeB.update()
                # show buttons
                config.screen.blit(self.playB.image, self.playB.rect)
                config.screen.blit(self.homeB.image, self.homeB.rect)

            while round(joystick.get_axis(0)):
                pygame.event.get()
                clock.tick(30)

            if jbuttons[js_lib["A"]]:
                while joystick.get_button(js_lib["A"]):
                    pygame.event.get()
                    clock.tick(30)
                if self.playB.highlight:
                    config.state = "game"
                else:
                    config.state = "main_menu"
                return

            pygame.display.flip()
            clock.tick(120)


class DeathButton(pygame.sprite.Sprite):
    """Sprite and state of death main_menu button"""
    def __init__(self, button_number, highlight):
        super(DeathButton, self).__init__()
        self.bn = button_number
        self.highlight = highlight
        self.ss = config.sheet_button
        self.image = pygame.transform.scale(self.ss.image_at((button_number * 56, highlight * 40, 56, 40), -1),
                                            (56 * config.sizer, 40 * config.sizer))
        offset = int(config.screen.get_width()/16) if button_number > 0 else -int(config.screen.get_width()/16)
        self.rect = self.image.get_rect(center=(config.screen.get_width()/2 + offset, config.screen.get_height() * 3/5))
        self.color = (0, 255, 0) if button_number > 0 else (255, 0, 0)

    def update(self):
        """toggle highlight on button on/off"""
        self.highlight = not self.highlight
        self.image = pygame.transform.scale(self.ss.image_at((self.bn * 56, self.highlight * 40, 56, 40), -1),
                                            (56 * config.sizer, 40 * config.sizer))
