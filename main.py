from initialise import *
from time import sleep, ticks_ms, ticks_diff


# Initialise Robot
ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED, oled = initialise()
angle(90, servo)

# Calibration
# oled.fill(0)
# oled.text("Press to Calibrate", 0, 0)
# oled.show()
# bootwait()
#
# oled.fill(0)
# oled.text("Calibrating...", 0, 0)
# oled.show()
# pwm = calibrate(motor_left, motor_right, enc, pwm=[30], time=1)
#
# oled.fill(0)
# oled.text("Done!", 0, 0)
# oled.show()
# sleep(1)

# Parameters
BASE_SPEED = 27
Kp = 0.7
Kd = 0.1
GAIN = 200
THRESHOLD = 2300
max_spd = 35

last_error = 0
last_seen = 0   # -1 = left, 0 = centre, 1 = right

white_start = None
WHITE_TIME = 150
environment = "START GARAGE"

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
def hallway_diff():
    sleep (0.3)
    r1 = ultrasonic.distance_mm()
    angle(60, servo)
    sleep(0.3)
    r2 = ultrasonic.distance_mm()
    angle(90, servo)
    sleep(0.3)
    if 0 < ultrasonic.distance_mm() < 80:
        return ""
    angle(130, servo)
    sleep(0.3)
    l1 = ultrasonic.distance_mm()
    angle(180, servo)
    sleep(0.3)
    l2 = ultrasonic.distance_mm()
    angle(23, servo)
    r = min(r1, r2)
    l = min(l1, l2)
    return l - r

# Start
stop()
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

    if environment == "START GARAGE":
        while (ir_l.read_u16() < THRESHOLD and ir_c.read_u16() < THRESHOLD and ir_r.read_u16() < THRESHOLD):
            if 0 < ultrasonic.distance_mm() < 50: #backwards threshold
                stop()
                sleep(0.5)
                motor_left.set_backwards()
                motor_right.set_backwards()
                motor_left.duty(30)
                motor_right.duty(30)
                sleep(0.7) # backwards time
            elif 0 < ultrasonic.distance_mm() < 100: #turn threshold
                motor_left.set_forwards()
                motor_right.set_backwards()
                motor_left.duty(30)
                motor_right.duty(30)
                sleep(0.3) #turn time
                if 0 < ultrasonic.distance_mm() > 200: #open end of garage threshold (just a big number)
                    sleep(0.5)
                    stop()
                    motor_left.set_forwards()
                    motor_right.set_forwards()
                    motor_left.duty(35)
                    motor_right.duty(30)
                    sleep(0.5) # extra turn time before going straight
            elif  ultrasonic.distance_mm() > 200: #same open threshold
                motor_left.set_forwards()
                motor_right.set_forwards()
                motor_left.duty(35)
                motor_right.duty(30)
        environment = " "
        continue

    # Track last seen
    if L > THRESHOLD:
        last_seen = -1
    elif R > THRESHOLD:
        last_seen = 1
    elif C > THRESHOLD:
        last_seen = 0

    # Check for 'all white'
    if L < THRESHOLD and C < THRESHOLD and R < THRESHOLD:
        stop()
        sleep(0.3) # time before checking - how long is a gap?
        L = ir_l.read_u16()
        C = ir_c.read_u16()
        R = ir_r.read_u16()
        if L > THRESHOLD and C > THRESHOLD and R > THRESHOLD: # Gap handling
            continue
        elif ticks_diff(ticks_ms(), white_start) > WHITE_TIME:
            set_motors(28, 28)
            sleep(0.2)
            stop()
        # Ultrasonic check
            angle(90, servo)
            c = 0 < ultrasonic.distance_mm() < 350

            angle(23, servo)
            sleep(0.6)
            r = 0 < ultrasonic.distance_mm() < 220

            angle(180, servo)
            sleep(0.6)
            l = 0 < ultrasonic.distance_mm() < 220

            angle(90, servo)

            if c and r and l:
                environment = "GARAGE"
            elif r and l:
                environment = "HALLWAY"
            elif c:
                environment = "DEAD END"
            else:
                environment = ""

            oled.fill(0)
            oled.text(environment, 0, 0)
            oled.show()
            sleep(1)
    else:
        white_start = None

    if 0 < ultrasonic.distance_mm() < 180:
        environment = "DEAD END"

    if L > THRESHOLD and C > THRESHOLD and R > THRESHOLD:
        environment = "ROUNDABOUT"

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
            oled.fill(0)
            oled.text("Fast Turning", 0, 0)
            oled.show()
            motor_left.set_forwards()
            motor_right.set_backwards()
            motor_left.duty(28)
            motor_right.duty(28)
            sleep(0.01)

        # Align to centre
        while not ir_c.read_u16() > THRESHOLD:
            oled.fill(0)
            oled.text("Slow Turning", 0, 0)
            oled.show()
            motor_left.set_forwards()
            motor_right.set_backwards()
            motor_left.duty(23)
            motor_right.duty(23)
            sleep(0.01)

        stop()
        sleep(1)
        environment = ""
        continue

    elif environment == "HALLWAY":
    # else:
        while (ir_l.read_u16() < THRESHOLD and ir_c.read_u16() < THRESHOLD and ir_r.read_u16() < THRESHOLD):
            stop()
            motor_left.set_forwards()
            motor_right.set_forwards()
            angle(23, servo)
            sleep(0.3)
            diff = hallway_diff()
            oled.fill_rect(0, 10, 100, 10, 0)
            oled.text(str(diff), 0, 10)
            oled.show()
            if diff == "":
                break
            if diff > -25 and diff < 25:
                motor_left.duty(30)
                motor_right.duty(30)
                sleep (0.3)
                stop()
            elif diff <= -10: #move over to the right
                motor_left.duty(30)
                sleep(0.25)
                motor_left.duty(0)
                #motor_right.duty(30)
                sleep(0.15)
            elif diff >= 10:
                motor_right.duty(30)
                sleep(0.25)
                motor_right.duty(0)
                #motor_left.duty(30)
                sleep(0.15)
            sleep(0.15)
        angle(90, servo)
        environment = " "
        set_motors(30,30)
        sleep(0.3)
        continue

    elif environment == "GARAGE":
        sleep(0.5)
        garage_dist_avg = 1000
        while garage_dist_avg > 80:
            set_motors(30,30)
            sleep(0.2) #time before next check
            garage_dist = []
            stop()
            for i in range(5): # Take N measurements and get the average - to help with issues I was having
                print(ultrasonic.distance_mm())
                garage_dist.append(ultrasonic.distance_mm())
                sleep(0.3)
            garage_dist_avg = sum(garage_dist) / len(garage_dist)
            print(f"Garage Distance: {garage_dist_avg}")
        break

    """Not well implemented roundabout code, though probably needs to be added back in and fixed up.
       Biggest issue was that it fired at the wrong points and just did donuts"""
    # elif environment == "ROUNDABOUT":
    #     counter = 0
    #     oled.fill(0)
    #     oled.text("Roundabout", 0, 0)
    #     oled.show()
    #     while counter < 2:
    #         if ir_l.read_u16() > THRESHOLD and ir_c.read_u16() >  THRESHOLD:
    #             counter += 1
    #         error = -pos
    #         derivative = error - last_error
    #         last_error = error
    #
    #         correction = (Kp * error) + (Kd * derivative)
    #
    #         left = BASE_SPEED - correction * GAIN
    #         right = BASE_SPEED + correction * GAIN
    #
    #         # Slow down on curves
    #         if abs(error) > 5:
    #             left *= 0.65
    #             right *= 0.65
    #
    #         set_motors(left, right)
    #         sleep(0.02)
    #     stop()
    #     while ir_c.read_u16() < THRESHOLD:
    #         oled.text("Turning Left", 0, 0)
    #         set_motors(10, 35)  # turn left
    #         sleep(0.02)
    #     environment = ""
    #     continue

    # Line Position (weighted average)
    wL = max(0, -THRESHOLD + L)
    wC = max(0, -THRESHOLD + C)
    wR = max(0, -THRESHOLD + R)

    total = wL + wC + wR
    print(total)

    if total < 10:
        pos = None
    else:
        pos = (wL*(-15) + wC*(0) + wR*(15)) / total # we multiply by 0 here?

    # If it loses the line
    if pos is None:
        while ir_l.read_u16() < THRESHOLD and ir_c.read_u16() < THRESHOLD and ir_r.read_u16() < THRESHOLD:
            oled.fill(0)
            stop()
            wall_dist = ultrasonic.distance_mm()
            if wall_dist > 40 and not wall_dist < 0: # HAS POTENTIAL TO MAKE TURNING FUNCTIONS SLOW. REMOVE THIS if it doesn't work.
                if last_seen == -1:
                    oled.text("Turning Left", 0, 0)
                    set_motors(10, 30)   # turn left
                    sleep(0.1)
                else: # last_seen == 1:
                    set_motors(30, 0)
                    oled.text("Turning Right", 0, 0)
                    sleep(0.1)
            else:
                motor_left.set_backwards()
                motor_right.set_backwards()
                motor_left.duty(30)
                motor_right.duty(30)
                sleep(0.1)
            # else:
            #     motor_left.set_backwards()
            #     motor_right.set_backwards()
            #     motor_left.duty(28)
            #     motor_right.duty(28)
            #     oled.text("Continuing Straight", 0, 0)
            #     sleep(0.02)
                oled.show()
                sleep(0.02)
        continue

    # PD control
    oled.fill(0)
    oled.text("Line Follow", 0, 0)
    oled.show()
    error = -pos
    derivative = error - last_error
    last_error = error

    correction = (Kp * error) + (Kd * derivative)

    left = BASE_SPEED - correction * GAIN
    right = BASE_SPEED + correction * GAIN

    # Slow down on curves
    if abs(error) > 5:
        left *= 0.65
        right *= 0.65

    set_motors(left, right)
    sleep(0.02)

LED.on()
oled.fill(0)
oled.text("YAYAYAYAYAYAYA", 0, 0)
oled.text("YAYAYAYAYAYAYA", 0, 10)
oled.text("YAYAYAYAYAYAYA", 0, 20)
oled.text("YAYAYAYAYAYAYA", 0, 30)
oled.text("YAYAYAYAYAYAYA", 0, 40)
oled.show()