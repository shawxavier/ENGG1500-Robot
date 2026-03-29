from initialise import *
from time import sleep, ticks_ms, ticks_diff

# ---------------- INITIALISE ----------------
ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED, oled = initialise()

angle(90, servo)

# ---------------- CALIBRATION ----------------
# oled.fill(0)
# oled.text("Press to Calibrate", 0, 0)
# oled.show()
# bootwait()
#
# oled.fill(0)
# oled.text("Calibrating...", 0, 0)
# oled.show()
# pwm = calibrate(motor_left, motor_right, enc, pwm=[30, 40, 50], time=0.5)
#
# oled.fill(0)
# oled.text("Done!", 0, 0)
# oled.show()
# sleep(1)

# ---------------- PARAMETERS ----------------
BASE_SPEED = 30
Kp = 0.045
Kd = 0.009
THRESHOLD = 3000

x_left = -15
x_centre = 0
x_right = 15

last_error = 0

max_spd = 50

# ---------------- DEAD-END TIMER ----------------
white_start = None
WHITE_TIME = 150  # ms

# ---------------- STATE FLAG ----------------
turned_once = False
environment = ""

# ---------------- HELPER FUNCTIONS ----------------
def read_line():
    wL = max(0, THRESHOLD - ir_l.read_u16())
    wC = max(0, THRESHOLD - ir_c.read_u16())
    wR = max(0, THRESHOLD - ir_r.read_u16())
    total = wL + wC + wR
    if total < 50:
        return None
    return (wL*x_left + wC*x_centre + wR*x_right) / total

def all_white():
    return (
        ir_l.read_u16() < THRESHOLD and
        ir_c.read_u16() < THRESHOLD and
        ir_r.read_u16() < THRESHOLD
    )

def centre_black():
    return ir_c.read_u16() > THRESHOLD

def any_black():
    return (
        ir_l.read_u16() > THRESHOLD or
        ir_c.read_u16() > THRESHOLD or
        ir_r.read_u16() > THRESHOLD
    )

def set_motors(left, right):
    left = max(0, min(max_spd, int(left)))
    right = max(0, min(max_spd, int(right)))
    motor_left.set_forwards()
    motor_right.set_forwards()
    motor_left.duty(left)
    motor_right.duty(right)

def stop():
    set_motors(0, 0)

# -------- TURN FUNCTIONS (true on-spot) --------
def turn_on_spot_fast():
    motor_left.set_forwards()
    motor_right.set_backwards()
    motor_left.duty(50)   # fast enough to turn
    motor_right.duty(50)

def turn_on_spot_slow():
    motor_left.set_forwards()
    motor_right.set_backwards()
    motor_left.duty(35)   # slow for precision alignment
    motor_right.duty(35)

# Ultrasonic Environment Detector
def US_detect():

    dist_thresh = 220
    set_motors(0, 0)
    angle(90, servo)
    c = ultrasonic.distance_mm() < dist_thresh
    angle(23, servo)
    sleep(0.8)
    r = ultrasonic.distance_mm() < dist_thresh
    angle(180, servo)
    sleep(0.8)
    l = ultrasonic.distance_mm() < dist_thresh
    angle(90, servo)

    if c and r and l:
        environment = "GARAGE"
    elif r and l:
        environment = "HALLWAY"
    elif c:
        environment = "DEAD END"
    else:
        environment = "NO LINE"

    oled.fill(0)
    oled.text(environment, 0, 0)
    oled.show()

    sleep(1)
    return environment

# ---------------- START ----------------
oled.fill(0)
oled.text("Press to Start", 0, 0)
oled.show()
bootwait()

oled.fill(0)
oled.text("Running...", 0, 0)
oled.show()
LED.on()

# ---------------- MAIN LOOP ----------------
while True:

    # ---------------- DEAD END DETECTION ----------------
    # if not turned_once and all_white():
    if all_white():
        if white_start is None:
            white_start = ticks_ms()

        elif ticks_diff(ticks_ms(), white_start) > WHITE_TIME:

            stop()
            sleep(0.5)

            environment = US_detect()

            if environment == "NO LINE":

                oled.fill(0)
                oled.text("TURNING", 0, 0)
                oled.show()

                # -------- FAST SPIN: find line --------
                while not any_black():
                    turn_on_spot_fast()
                    sleep(0.01)

                # -------- SLOW ALIGNMENT: centre sensor --------
                while not centre_black():
                    turn_on_spot_slow()
                    sleep(0.01)

                stop()  # exactly on line
                sleep(2)  # wait 2 seconds before resuming forward motion

                turned_once = True
                white_start = None
                environment = ""
                continue

    else:
        white_start = None

    # ---------------- NORMAL LINE FOLLOWING ----------------
    pos = read_line()

    if pos is None:
        continue

    error = -pos
    derivative = error - last_error
    correction = (Kp * error) + (Kd * derivative)
    last_error = error

    left = BASE_SPEED + correction * 800
    right = BASE_SPEED - correction * 800

    if abs(error) > 8:
        left *= 0.75
        right *= 0.75

    set_motors(left, right)

    # ---------------- DISPLAY ----------------
    oled.fill(0)
    oled.text("FOLLOWING", 0, 0)
    oled.text(f"L:{ir_l.read_u16()}", 0, 10)
    oled.text(f"C:{ir_c.read_u16()}", 0, 20)
    oled.text(f"R:{ir_r.read_u16()}", 0, 30)
    oled.text(f"Pos: {pos}", 0, 50)
    oled.show()

    sleep(0.02)