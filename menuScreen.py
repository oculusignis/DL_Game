import pygame
import spriteSheet
from pygame.locals import (K_a, K_d, K_ESCAPE, K_SPACE, KEYDOWN, QUIT)


class MenuButton(pygame.sprite.Sprite):
    """Sprite for a menu_running button"""

    def __init__(self, button_number, highlight, window_stats):
        super(MenuButton, self).__init__()
        screenw, screenh, self.size_multiplier = window_stats
        self.b_number = button_number
        self.highlight = highlight
        self.ss = spriteSheet.SpriteSheet("resources/MenuButtons.png")
        self.image = self.ss.image_at((button_number * 56, highlight * 40, 56, 40))
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


class Menu:
    """manages menu_running buttons and their states"""

    def __init__(self, screen: pygame.display, sizer):
        self.active = 0
        self.states = {0: "play", 1: "settings", 2: "exit"}
        window_stats = (screen.get_width(), screen.get_height(), sizer)
        play_button = MenuButton(0, 1, window_stats)
        setting_button = MenuButton(1, 0, window_stats)
        exit_button = MenuButton(2, 0, window_stats)
        self.buttons = (play_button, setting_button, exit_button)
        self.screen = screen

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

    def menu_loop(self, program_state):
        """runs the menu"""
        menu_color = (0xeb, 0xd2, 0xbe)
        while True:
            self.screen.fill(menu_color)

            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        program_state["menu"] = False
                        return
                    if event.key == K_SPACE:
                        if self.states[self.active] is "play":
                            program_state["menu"] = False
                            program_state["game"] = True
                            return
                        elif self.states[self.active] is "settings":
                            # TODO
                            pass
                        elif self.states[self.active] is "exit":
                            program_state["menu"] = False
                            return
                elif event.type == QUIT:
                    program_state["menu"] = False
                    return

            self.update(events)
            for button in self.buttons:
                self.screen.blit(button.image, button.rect)
            pygame.display.flip()
