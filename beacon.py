import radio
import music
from utime import sleep_ms
from microbit import display, Image


def main():
    POWER = 7
    DELAY = 1500
    MAX_SIGNAL_TONE = 2000
    MIN_SIGNAL_TONE = 500
    PITCH_DURATION = 100

    radio.on()
    radio.config(
        group=42,
        length=1,
        queue=1,
        data_rate=radio.RATE_1MBIT,
        power=POWER,
    )

    while True:
        radio.send('')
        display.set_pixel(2, 2, 9)
        sleep_ms(100)
        display.clear()
        details = radio.receive_full()
        if details:
            _, rssi, _ = details
            tone = MAX_SIGNAL_TONE - abs(rssi * 15)
            if tone < MIN_SIGNAL_TONE:
                tone = MIN_SIGNAL_TONE
            music.pitch(tone, PITCH_DURATION, wait=False)
            display.show(Image().invert(), delay=PITCH_DURATION, wait=False, clear=True)
        sleep_ms(DELAY)
