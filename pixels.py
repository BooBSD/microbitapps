import music
from random import randint, random
from microbit import display, sleep, button_a, button_b, pin_logo


def main():
    DISPLAY = ((0, 4), (0, 4))
    PIXEL_BRIGHTNESS_LEVELS = (1, 9)
    AUTO_RANDOM_LEVEL_CHANGE = 0.005
    SLEEP_RANGE = (0, 100)
    r = 0
    s = 0
    sleep_max = 0
    auto = True
    music.play(music.BA_DING)
    while True:
        if auto and (random() < AUTO_RANDOM_LEVEL_CHANGE):
            r = random()
            music.pitch(400, 1, wait=False)
        if auto and (random() < AUTO_RANDOM_LEVEL_CHANGE):
            s = random()
            music.pitch(800, 1, wait=False)
        if auto and (random() < AUTO_RANDOM_LEVEL_CHANGE):
            sleep_max = randint(*SLEEP_RANGE)
            music.pitch(1200, 1, wait=False)
        if button_a.was_pressed():
            r = random()
            auto = False
        elif button_b.was_pressed():
            s = random()
            auto = False
        elif pin_logo.is_touched():
            sleep_max = randint(*SLEEP_RANGE)
            auto = False
        display.set_pixel(randint(*DISPLAY[0]), randint(*DISPLAY[1]), randint(*PIXEL_BRIGHTNESS_LEVELS) if random() < r else 0)
        if random() < s:
            sleep(randint(0, sleep_max))
