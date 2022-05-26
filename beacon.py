import radio
import music
from utime import sleep_ms, ticks_ms, ticks_diff
from microbit import display, Image, button_a, button_b, pin_logo, speaker
from micropython import const


def cycle(iter, reverse=False):
    iter = list(iter)
    if reverse:
        iter = iter + list(reversed(iter[1:-1]))
    while True:
        for i in iter:
            yield i


def get_brightness(integer=False):
    BRIGHTNESS_MIN = const(4)
    light = display.read_light_level()
    if integer:
        return int((light / 51) + BRIGHTNESS_MIN)
    return ((light / 42.5) + BRIGHTNESS_MIN) / 10


POWER_IMAGE_PATTERN = (
    4, 5, 6, 7, 8,
    3, 4, 5, 6, 7,
    2, 3, 4, 5, 6,
    1, 2, 3, 4, 5,
    0, 1, 2, 3, 4,
)


def get_power_image(power):
    pixels = bytearray((9 if p <= power else 0 for p in POWER_IMAGE_PATTERN))
    return Image(5, 5, pixels) * get_brightness(integer=True)


def main():
    POWER = cycle(range(-1, 8 + 1), reverse=True)
    CHANNEL = const(0)
    DELAY = const(1000)
    MAX_SIGNAL_TONE = const(3200)
    RSSI_BIG_IMAGE = const(-80)
    PITCH_DURATION = const(50)
    ICON_DELAY = const(300)
    RADIO_CONFIG = {
        'channel': CHANNEL,
        'group': 42,
        'length': 1,
        'queue': 1,
        'data_rate': radio.RATE_1MBIT,
    }

    for _ in range(18):
        power = next(POWER)  # Starting power is 0 (not -1).
    sound = True
    flash = True

    radio.on()
    radio.config(power=power, **RADIO_CONFIG)

    last = ticks_ms()
    while True:
        if pin_logo.is_touched():
            flash = not flash
            image = Image.HEART if flash else Image.NO
            display.show(image * get_brightness(), delay=ICON_DELAY, wait=True, clear=True)
        elif button_a.was_pressed():
            power = next(POWER)
            if power == -1:
                display.show(Image.NO * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
            else:
                radio.config(power=power, **RADIO_CONFIG)
                display.show(get_power_image(power) * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
            if sound:
                speaker.on()
                music.pitch(800 + (power * 100), PITCH_DURATION, wait=True)
                speaker.off()  # Trying to optimize power consumption
        elif button_b.was_pressed():
            sound = not sound
            image = Image.MUSIC_QUAVER if sound else Image.NO
            display.show(image * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
            if sound:
                display.show(Image.MUSIC_QUAVER * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
                speaker.on()
                music.play(['b5:1', 'e6:2'], wait=True)
                speaker.off()  # Trying to optimize power consumption
        if ticks_diff(ticks_ms(), last) > DELAY:
            last = ticks_ms()
            if power == -1:
                sleep_ms(100)
            else:
                radio.send('B')
                display.set_pixel(2, 2, get_brightness(integer=True))
                sleep_ms(100)
                display.clear()
            details = radio.receive_full()
            if details:
                _, rssi, _ = details
                if flash:
                    image = Image.HEART if rssi > RSSI_BIG_IMAGE else Image.HEART_SMALL
                    display.show(image * get_brightness(), delay=PITCH_DURATION, wait=False, clear=True)
                if sound:
                    tone = int((1 / abs(rssi)) ** 4 * 20000000000)
                    if tone > MAX_SIGNAL_TONE:
                        tone = MAX_SIGNAL_TONE
                    speaker.on()
                    music.pitch(tone, PITCH_DURATION, wait=True)
                    speaker.off()  # Trying to optimize power consumption
        sleep_ms(100)


if __name__ == '__main__':
    main()
