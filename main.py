# Crazy Commute — Wanderlust Gaming Co.
# --------------------------------------
# Hardware:
#   RGB LED 1       → GP0, GP1, GP2
#   RGB LED 2       → GP8, GP9, GP10
#   Speaker         → GP7
#   5-way switch    → GP11 (up), GP12 (down), GP13 (left), GP14 (right), GP15 (press)
#   Regular LEDs    → GP16, GP17, GP18, GP19
#   Servo (bird)    → GP28
#   Servo (ped)     → GP27
#   Servo (railroad)→ GP26
#   Red light button→ GP5

from machine import Pin, PWM
from time import sleep
from random import randint

# ── RGB LEDs ────────────────────────────────────────────────
red_led1   = PWM(Pin(0))
green_led1 = PWM(Pin(1))
blue_led1  = PWM(Pin(2))

red_led2   = PWM(Pin(8))
green_led2 = PWM(Pin(9))
blue_led2  = PWM(Pin(10))

for led in [red_led1, green_led1, blue_led1, red_led2, green_led2, blue_led2]:
    led.freq(1000)

def set_color(red, green, blue):
    red_led1.duty_u16(int(red * 65535 / 255))
    green_led1.duty_u16(int(green * 65535 / 255))
    blue_led1.duty_u16(int(blue * 65535 / 255))
    red_led2.duty_u16(int(red * 65535 / 255))
    green_led2.duty_u16(int(green * 65535 / 255))
    blue_led2.duty_u16(int(blue * 65535 / 255))

# ── SPEAKER ─────────────────────────────────────────────────
speaker = PWM(Pin(7), duty_u16=32768)

# ── 5-WAY SWITCH ────────────────────────────────────────────
up    = Pin(11, Pin.IN, Pin.PULL_DOWN)
down  = Pin(12, Pin.IN, Pin.PULL_DOWN)
left  = Pin(13, Pin.IN, Pin.PULL_DOWN)
right = Pin(14, Pin.IN, Pin.PULL_DOWN)
press = Pin(15, Pin.IN, Pin.PULL_DOWN)

# ── REGULAR LEDs ────────────────────────────────────────────
led_1 = Pin(19, Pin.OUT)
led_2 = Pin(18, Pin.OUT)
led_3 = Pin(17, Pin.OUT)
led_4 = Pin(16, Pin.OUT)

led_1.off()
led_2.off()
led_3.off()
led_4.off()

# ── SERVOS ──────────────────────────────────────────────────
max_duty  = 7864
min_duty  = 1802
half_duty = int((max_duty + min_duty) / 2)
frequency = 50

railroad_crossing = PWM(Pin(26))
bird              = PWM(Pin(28))
pedestrian        = PWM(Pin(27))

railroad_crossing.freq(frequency)
railroad_crossing.duty_u16(max_duty)

bird.freq(frequency)
bird.duty_u16(max_duty)

pedestrian.freq(frequency)
pedestrian.duty_u16(min_duty)

# ── RED LIGHT BUTTON ────────────────────────────────────────
red_light_button = Pin(5, Pin.IN, Pin.PULL_UP)

# ── STATE ───────────────────────────────────────────────────
timer         = 0
time_bird     = 0
time_ped      = 0
time_cross    = 0
bird_indicator  = False
ped_indicator   = False
cross_indicator = False
led_sequence    = []
switch          = []
num_switch_pushes = 0

# ── HELPERS ─────────────────────────────────────────────────
def tick_timers(dt):
    global timer, time_bird, time_ped, time_cross
    timer += dt
    if bird_indicator:
        time_bird += dt
    if cross_indicator:
        time_cross += dt
    if ped_indicator:
        time_ped += dt

def reset_servo(servo, duty, dt=2):
    servo.duty_u16(duty)
    tick_timers(dt)
    sleep(dt)

def flash_all_leds(times=4, interval=0.5):
    for _ in range(times):
        for l in [led_1, led_2, led_3, led_4]:
            l.on()
        sleep(interval)
        for l in [led_1, led_2, led_3, led_4]:
            l.off()
        sleep(interval)

# ── MAIN LOOP ───────────────────────────────────────────────
while True:

    # Traffic light
    if timer < 2:
        set_color(0, 255, 0)        # green
    elif 20 < timer < 22:
        set_color(255, 100, 0)      # yellow
    elif 25 < timer < 27:
        set_color(255, 0, 0)        # red
    elif timer > 35:
        timer = 0

    # Reset servos after 30 seconds
    if time_bird >= 30:
        reset_servo(bird, max_duty)
        time_bird = 0
        bird_indicator = False

    if time_ped >= 30:
        reset_servo(pedestrian, min_duty)
        time_ped = 0
        ped_indicator = False

    if time_cross >= 30:
        reset_servo(railroad_crossing, max_duty)
        time_cross = 0
        cross_indicator = False

    # Red light button — flash all LEDs
    if red_light_button.value() == 0:
        flash_all_leds(times=4, interval=0.5)

    # Press center — generate new LED sequence
    if press.value() == 1:
        led_sequence = []
        switch = []
        num_switch_pushes = 0
        for i in range(6):
            x = randint(16, 19)
            Pin(x, Pin.OUT).on()
            tick_timers(0.75)
            sleep(0.75)
            Pin(x, Pin.OUT).off()
            tick_timers(0.75)
            sleep(0.75)
            led_sequence.append(x)

    # 5-way switch inputs
    for value, pin_val, led, seq_val in [
        (up,    1, led_1, 19),
        (left,  1, led_2, 18),
        (down,  1, led_3, 17),
        (right, 1, led_4, 16),
    ]:
        if value.value() == pin_val:
            led.on()
            tick_timers(0.5)
            sleep(0.5)
            led.off()
            switch.append(seq_val)
            num_switch_pushes += 1

    # Sequence correct
    if num_switch_pushes == 6 and switch == led_sequence:
        for l in [led_1, led_2, led_3, led_4]:
            l.on()
            sleep(0.5)
        for l in [led_1, led_2, led_3, led_4]:
            l.off()
        sleep(0.3)
        for l in [led_1, led_2, led_3, led_4]:
            l.on()
        sleep(0.3)
        for l in [led_1, led_2, led_3, led_4]:
            l.off()

        for freq in [525, 700, 800]:
            speaker.init(freq=freq)
            sleep(0.25)
            speaker.deinit()
            sleep(0.25)

        while up.value() == 0 and left.value() == 0 and down.value() == 0:
            tick_timers(0.01)
            sleep(0.01)

        if up.value() == 1:
            reset_servo(pedestrian, half_duty)
            ped_indicator = True

        if right.value() == 1:
            reset_servo(bird, int(half_duty * 1.3))
            bird_indicator = True

        if down.value() == 1:
            reset_servo(railroad_crossing, half_duty)
            cross_indicator = True

        num_switch_pushes = 0
        switch = []

    # Sequence wrong
    elif num_switch_pushes == 6:
        for l in [led_1, led_2, led_3, led_4]:
            l.on()
        sleep(1)
        for l in [led_1, led_2, led_3, led_4]:
            l.off()
        num_switch_pushes = 0
        switch = []

        for freq in [140, 240, 100]:
            speaker.init(freq=freq)
            sleep(0.25)
            speaker.deinit()
            sleep(0.25)

    tick_timers(0.1)
    sleep(0.1)
