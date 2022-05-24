import radio
import music
from utime import sleep_ms, ticks_ms, ticks_diff
from microbit import display, Image, button_a, button_b, pin0, speaker
from micropython import const


def cycle(iter):
    iter = list(iter)
    new_iter = iter + list(reversed(iter[1:-1]))
    while True:
        for i in new_iter:
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
    POWER = cycle(range(0, 8 + 1))
    CHANNEL = const(0)
    DELAY = const(1000)
    MAX_SIGNAL_TONE = const(3200)
    PITCH_DURATION = const(50)
    ICON_DELAY = const(300)
    RADIO_CONFIG = {
        'channel': CHANNEL,
        'group': 42,
        'length': 1,
        'queue': 1,
        'data_rate': radio.RATE_1MBIT,
    }

    power = next(POWER)
    sound = True

    radio.on()
    radio.config(power=power, **RADIO_CONFIG)

    last = ticks_ms()
    while True:
        if button_a.was_pressed():
            power = next(POWER)
            radio.config(power=power, **RADIO_CONFIG)
            display.show(get_power_image(power) * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
            if sound:
                music.pitch(800 + (power * 100), PITCH_DURATION, wait=False)
        elif button_b.was_pressed():
            sound = not sound
            if sound:
                music.play(['b5:1', 'e6:2'], wait=False)
                display.show(Image.MUSIC_QUAVER * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
                speaker.on()
            else:
                display.show(Image.NO * get_brightness(), delay=ICON_DELAY, wait=False, clear=True)
                speaker.off()
                # Dirty hack to turn off external buzzer
                pin0.write_digital(0)
        if ticks_diff(ticks_ms(), last) > DELAY:
            last = ticks_ms()
            radio.send('B')
            display.set_pixel(2, 2, get_brightness(integer=True))
            sleep_ms(100)
            display.clear()
            details = radio.receive_full()
            if details:
                _, rssi, _ = details
                tone = int((1 / abs(rssi)) ** 4 * 20000000000)
                if tone > MAX_SIGNAL_TONE:
                    tone = MAX_SIGNAL_TONE
                if sound:
                    music.pitch(tone, PITCH_DURATION, wait=False)
                display.show(Image.HEART * get_brightness(), delay=PITCH_DURATION, wait=False, clear=True)
        sleep_ms(100)


if __name__ == '__main__':
    main()
