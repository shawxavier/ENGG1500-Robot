from initialise import *
from time import sleep, ticks_ms, ticks_diff

# Calibration
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

# Parameters
ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED, oled = initialise()
angle(90, servo)

BASE_SPEED = 18
Kp = 0.06
Kd = 0.02
GAIN = 220
THRESHOLD = 2500
max_spd = 36

last_error = 0
last_seen = 0   # -1 = left, 0 = centre, 1 = right

white_start = None
WHITE_TIME = 150
environment = ""
integral = 0

# Motor Function
def set_motors(left, right):
    left = max(0, min(max_spd, int(left)))
    right = max(0, min(max_spd, int(right)))
    motor_left.set_forwards()
    motor_right.set_forwards()
    motor_left.duty(left)
    motor_right.duty(right)

def stop():
    set_motors(0, 0)

# Hallway Functions
def enc_diff():
    return enc.get_left() - enc.get_right()

def enc_pid(int):
    L = ir_l.read_u16()
    C = ir_c.read_u16()
    R = ir_r.read_u16()
    while L < THRESHOLD and C < THRESHOLD and R < THRESHOLD:
        L = ir_l.read_u16()
        C = ir_c.read_u16()
        R = ir_r.read_u16()
        kp = 0.2
        ki = 0.2
        kd = 0.02
        error = enc_diff()
        prev_error = error
        int += error * 0.1
        derv = (prev_error - error) / 0.1
        cont = error * kp + ki * int + kd * derv
        set_motors(BASE_SPEED - cont * GAIN, BASE_SPEED + cont * GAIN)
        sleep(0.1)
    return int

# Start
oled.fill(0)
oled.text("Press to Start", 0, 0)
oled.show()
bootwait()

oled.fill(0)
oled.text("Running...", 0, 0)
oled.show()
LED.on()

# Main loop
while True:

    # Read the sensors
    L = ir_l.read_u16()
    C = ir_c.read_u16()
    R = ir_r.read_u16()

    # Track last seen
    if L > THRESHOLD:
        last_seen = -1
    elif R > THRESHOLD:
        last_seen = 1
    elif C > THRESHOLD:
        last_seen = 0

    # Check for 'all white'
    if L < THRESHOLD and C < THRESHOLD and R < THRESHOLD:
        if white_start is None:
            white_start = ticks_ms()
        elif ticks_diff(ticks_ms(), white_start) > WHITE_TIME:
            stop()
            sleep(0.3)

            # Ultrasonic check
            angle(90, servo)
            c = ultrasonic.distance_mm() < 220

            angle(23, servo)
            sleep(0.6)
            r = ultrasonic.distance_mm() < 220

            angle(180, servo)
            sleep(0.6)
            l = ultrasonic.distance_mm() < 220

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
    else:
        white_start = None

    if ultrasonic.distance_mm() < 120:
        environment = "DEAD END"

    # This is for special cases
    if environment == "NO LINE" or environment == "DEAD END":
        # If we are at a dead end, turn a bit first
        if environment == "DEAD END":
            motor_left.set_forwards()
            motor_right.set_backwards()
            motor_left.duty(28)
            motor_right.duty(28)
            sleep(0.5)
        # Turn until line found
        while not (ir_l.read_u16() > THRESHOLD or ir_c.read_u16() > THRESHOLD or ir_r.read_u16() > THRESHOLD):
            motor_left.set_forwards()
            motor_right.set_backwards()
            motor_left.duty(28)
            motor_right.duty(28)
            sleep(0.01)

        # Align to centre
        while not ir_c.read_u16() > THRESHOLD:
            motor_left.set_forwards()
            motor_right.set_backwards()
            motor_left.duty(20)
            motor_right.duty(20)
            sleep(0.01)

        stop()
        sleep(1)
        environment = ""
        continue

    # elif environment == "HALLWAY":
    else:
        enc.clear_count()
        integral = enc_pid(integral)
        continue

    # Line Position (weighted average)
    wL = max(0, THRESHOLD - L)
    wC = max(0, THRESHOLD - C)
    wR = max(0, THRESHOLD - R)

    total = wL + wC + wR

    if total < 80:
        pos = None
    else:
        pos = (wL*(-15) + wC*(0) + wR*(15)) / total

    # If it loses the line
    if pos is None:
        if last_seen == -1:
            set_motors(10, 22)   # turn left
        elif last_seen == 1:
            set_motors(20, 10)   # turn right (but a bit slower)
        else:
            set_motors(12, 12)
        sleep(0.02)
        continue

    # PD control
    error = -pos
    derivative = error - last_error
    last_error = error

    correction = (Kp * error) + (Kd * derivative)

    left = BASE_SPEED + correction * GAIN
    right = BASE_SPEED - correction * GAIN

    # Slow down on curves
    if abs(error) > 5:
        left *= 0.65
        right *= 0.65

    set_motors(left, right)
    sleep(0.02)