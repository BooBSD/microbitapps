import radio
import music
import math
from utime import sleep_ms, ticks_ms, ticks_diff
from microbit import display, Image, button_a, button_b


def cycle(iter):
    while True:
        for i in iter:
            yield i


def main():
    POWER = cycle(range(0, 7 + 1))
    CHANNEL = cycle(range(0, 83 + 1))
    DELAY = 1000
    MAX_SIGNAL_TONE = 3200
    PITCH_DURATION = 80
    RADIO_CONFIG = {
        'group': 42,
        'length': 1,
        'queue': 1,
        'data_rate': radio.RATE_1MBIT,
    }

    power = next(POWER)
    channel = next(CHANNEL)

    radio.on()
    radio.config(power=power, channel=channel, **RADIO_CONFIG)

    last = ticks_ms()
    while True:
        if button_a.was_pressed():
            power = next(POWER)
            radio.config(power=power, channel=channel, **RADIO_CONFIG)
            display.show(power, delay=300, wait=False, clear=True)
        elif button_b.was_pressed():
            channel = next(CHANNEL)
            radio.config(power=power, channel=channel, **RADIO_CONFIG)
            display.show(channel, delay=300, wait=False, clear=True)
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
                music.pitch(tone, PITCH_DURATION, wait=False)
                display.show(Image().invert(), delay=PITCH_DURATION, wait=False, clear=True)
        sleep_ms(100)
