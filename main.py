import os
from microbit import display, Image, accelerometer, button_a, button_b, sleep
from micropython import const


MAX_APPS = const(25)
BRIGHTNESS_APP = const(5)
BRIGHTNESS_CURSOR = const(9)
COORDINATE_DIFF = const(30)
COORDINATE_CHECK_DELAY = const(20)
COORDINATE_LEVELS = (300, 150, 0, -150, -300)


def get_coordinate(a):
    for i, n in enumerate(COORDINATE_LEVELS):
        if i == 0 and a > (n - COORDINATE_DIFF):
            return i
        elif i == (len(COORDINATE_LEVELS) - 1) and a < (n + COORDINATE_DIFF):
            return i
        elif (n - COORDINATE_DIFF) < a < (n + COORDINATE_DIFF):
            return i
    return None


modules = map(__import__, sorted((m.rstrip('.py') for m in os.listdir() if m != 'main.py' and m.endswith('.py')))[:MAX_APPS])
apps = {(i % 5, i // 5): m for i, m in enumerate(modules)}


def render(x, y):
    display.clear()
    for app_x, app_y in apps.keys():
        display.set_pixel(app_x, app_y, BRIGHTNESS_APP)
    display.set_pixel(x, y, BRIGHTNESS_CURSOR)


def no():
    display.show(Image.NO)
    sleep(200)
    render(X, Y)


state = [0, 0]
X, Y = 2, 2


while True:
    x, y, _ = accelerometer.get_values()
    xx = get_coordinate(x)
    yy = get_coordinate(y)
    if xx is not None:
        X = xx
    if yy is not None:
        Y = yy
    
    if state != [X, Y]:
        render(X, Y)
    if button_a.was_pressed():
        app = apps.get((X, Y))
        if app is not None:
            app_name = getattr(app, '__doc__', app.__name__.replace('_', ' '))
            display.scroll(app_name, delay=100)
        else:    
            no()
    elif button_b.was_pressed():
        app = apps.get((X, Y))
        if app is not None:
            display.clear()
            break
        no()
    state = [X, Y]
    sleep(COORDINATE_CHECK_DELAY)

app.main()
