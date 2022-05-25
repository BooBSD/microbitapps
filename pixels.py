import music
from random import randint, random
from microbit import display, speaker, accelerometer, button_a, button_b, pin_logo, sleep


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
            speaker.off()
        elif button_b.was_pressed():
            s = random()
            auto = False
            speaker.off()
        elif pin_logo.is_touched():
            sleep_max = randint(*SLEEP_RANGE)
            auto = False
            speaker.off()
        elif not auto and accelerometer.was_gesture('shake'):
            auto = True
            speaker.on()
            music.play(music.BA_DING)
        display.set_pixel(randint(*DISPLAY[0]), randint(*DISPLAY[1]), randint(*PIXEL_BRIGHTNESS_LEVELS) if random() < r else 0)
        if random() < s:
            sleep(randint(0, sleep_max))


if __name__ == '__main__':
    main()
