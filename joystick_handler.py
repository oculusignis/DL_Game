import pygame
import config

usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}

# TODO use  this in --------------------- -> MAIN, MENU, PLAYER AND GAME <- ------------------------------


# TODO function: return connected joysticks

# TODO function: return master joystick


# TODO wait till no input
def js_wait_normal_all():
    """waits until no 'Start' or 'A' is pressed on any joystick"""
    clock = pygame.time.Clock()
    done = False

    while not done:
        pygame.event.get()

        for x in range(pygame.joystick.get_count()):
            jos = pygame.joystick.Joystick(x)
            jos.init()

            if jos.get_button(usb_lib["Start"]) or jos.get_button(usb_lib["A"]):
                done = False
                break
            else:
                done = True
        clock.tick(20)


def js_wait_normal(joystick: pygame.joystick.Joystick):
    """waits till joystick's 'Start' and 'A' aren't pressed"""
    clock = pygame.time.Clock()
    done = False
    while not done:
        pygame.event.get()
        if joystick.get_button((usb_lib["Start"])) or joystick.get_button(usb_lib["A"]):
            pass
        else:
            return
        clock.tick(20)


def js_nocontroller():
    """displays Error, until a joystick is connected"""
    clock = pygame.time.Clock()
    pygame.joystick.init()

    # display icon
    rect = config.screen.get_rect().copy()
    surf1 = config.screen.copy()
    surf1.set_alpha(100)

    # TODO make icon "no controller" instead of text message
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    textbitmap = font.render("NO CONTROLLER", True, (0, 0, 0))
    config.screen.blit(textbitmap, (config.screen.get_width()/2 - 160, config.screen.get_height()/2 - 20))
    pygame.display.flip()

    # wait until connected
    while pygame.joystick.get_count() < 1:
        pygame.event.get()
        clock.tick(20)


# TODO joystick config
def js_config():
    """returns specific config library"""
    pass

# TODO return library with above config  -> auto detection? <-


# TODO remove after testing
if __name__ == "__main__":
    config.__init__()
    config.screen.fill((200, 230, 230))
    pygame.display.flip()
    pygame.event.get()
    pygame.joystick.init()

    clk = pygame.time.Clock()

    js = pygame.joystick.Joystick(0)
    while not js.get_button(usb_lib["A"]):
        pygame.event.get()
        clk.tick(20)

    js_wait_normal_all()

    pygame.quit()
