import radio
import music
from utime import sleep_ms, ticks_ms, ticks_diff
from microbit import display, Image, button_a, button_b, pin0, pin_speaker


def cycle(iter):
    while True:
        for i in iter:
            yield i


def main():
    POWER = cycle(range(0, 7 + 1))
    CHANNEL = 0
    DELAY = 1000
    MAX_SIGNAL_TONE = 3200
    PITCH_DURATION = 80
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
            display.show(power, delay=ICON_DELAY, wait=False, clear=True)
        elif button_b.was_pressed():
            sound = not sound
            if not sound:
                # Dirty hack to turn off external buzzer
                pin0.write_digital(0)
                pin_speaker.write_digital(0)
            display.show(Image.MUSIC_QUAVER if sound else Image.NO, delay=ICON_DELAY, wait=False, clear=True)
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
                display.show(Image().invert(), delay=PITCH_DURATION, wait=False, clear=True)
        sleep_ms(100)
