import radio
import music
from utime import sleep_ms, ticks_ms, ticks_diff
from microbit import display, Image, button_a, button_b, pin0, pin_speaker


def cycle(iter):
    iter = list(iter)
    new_iter = iter + list(reversed(iter[1:-1]))
    while True:
        for i in new_iter:
            yield i


POWER_IMAGE_PATTERN = (
    4, 5, 6, 7, 8,
    3, 4, 5, 6, 7,
    2, 3, 4, 5, 6,
    1, 2, 3, 4, 5,
    0, 1, 2, 3, 4,
)


def get_power_image(power):
    pixels = bytearray((9 if p <= power else 0 for p in POWER_IMAGE_PATTERN))
    return Image(5, 5, pixels)


def main():
    POWER = cycle(range(0, 7 + 1))
    CHANNEL = 0
    DELAY = 1000
    MAX_SIGNAL_TONE = 3200
    PITCH_DURATION = 50
    ICON_DELAY = 300
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
            display.show(get_power_image(power), delay=ICON_DELAY, wait=False, clear=True)
            if sound:
                music.pitch(800 + (power * 100), PITCH_DURATION, wait=False)
        elif button_b.was_pressed():
            sound = not sound
            if sound:
                display.show(Image.MUSIC_QUAVER, delay=ICON_DELAY, wait=False, clear=True)
                music.play(['b5:1', 'e6:2'], wait=False)
            else:
                # Dirty hack to turn off external buzzer
                pin0.write_digital(0)
                pin_speaker.write_digital(0)
                display.show(Image.NO, delay=ICON_DELAY, wait=False, clear=True)
        if ticks_diff(ticks_ms(), last) > DELAY:
            last = ticks_ms()
            radio.send('B')
            display.set_pixel(2, 2, 9)
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
                display.show(Image.HEART, delay=PITCH_DURATION, wait=False, clear=True)
        sleep_ms(100)


if __name__ == '__main__':
    main()
