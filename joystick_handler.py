import pygame

usb_lib = {"X": 0, "A": 1, "B": 2, "Y": 3, "LS": 4, "RS": 5, "Select": 8, "Start": 9}

# TODO use  this in -------------------------- -> MAIN, MENU AND GAME <- ------------------------------


# TODO wait till no input
def js_wait_all():
    """waits until no 'Start' or 'A' is pressed on any joystick"""
    js_num = pygame.joystick.get_count()
    clock = pygame.time.Clock()
    done = False

    while not done:
        pygame.event.get()
        js_num = pygame.joystick.get_count()

        for x in range(js_num):
            js = pygame.joystick.Joystick(x)
            js.init()

            if js.get_button(usb_lib["Start"]) or js.get_button(usb_lib["A"]):
                break
            else:
                done = True
        clock.tick(20)


def js_wait(joystick: pygame.joystick.Joystick):
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


def js_connect(screen: pygame.Surface, mult: int):
    """displays Error, until a joystick is connected"""
    clock = pygame.time.Clock()
    pygame.joystick.init()

    # display icon
    rect = screen.get_rect().copy()
    surf1 = screen.copy()
    surf1.set_alpha(100)

    # TODO make icon "no controller" instead of text message
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    textbitmap = font.render("NO CONTROLLER", True, (0, 0, 0))
    screen.blit(textbitmap, (screen.get_height()/2, screen.get_width()/2))

    # wait until connected
    while pygame.joystick.get_count() < 1:
        clock.tick(20)


# TODO joystick config
def js_config():
    """returns specific config library"""
    pass

# TODO return library with above config  -> auto detection? <-
