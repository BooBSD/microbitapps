import speech
from microbit import display, Image, sleep, microphone, accelerometer, SoundEvent
from random import choice, randint


AWAKE = (
    "Good morning Mila!",
    "Wake up!",
    "Please, give me coffee!",
)

SLEEP = (
    "It's time to sleep!",
    "I want to sleep!",
    "Please, quiter!"
)


def main():
    last_light = 100
    while True:
        light = display.read_light_level()
        if light == 0:
            display.show(Image.ASLEEP * 0.2)
            if microphone.was_event(SoundEvent.LOUD) or accelerometer.was_gesture('shake'):
                display.show(Image.ANGRY * 0.5)
                sleep(randint(1, 20) * 100)
                speech.say(choice(SLEEP))
        else:
            display.show(Image.HAPPY)
            if last_light == 0:
                for _ in range(randint(1, 5)):
                    sleep(randint(1, 5) * 1000)
                    speech.say(choice(AWAKE))
        last_light = light
        sleep(1000)


if __name__ == '__main__':
    main()
