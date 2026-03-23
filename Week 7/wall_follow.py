from initialise import *
from time import sleep

print("1")


# Set variables from the initialise script
ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED, oled = initialise()

angle(90, servo)

motor_left.duty(0)
motor_right.duty(0)

oled_text("Press to Calibrate", oled)  # calibrate gets the same motor speeds for both motors, and puts them in the pwm dictionary
bootwait()
oled_text("Calibrating...", oled)
pwm = calibrate(motor_left, motor_right, enc, time=0.5, pwm=[40,50])
oled_text("Calibration Complete!", oled)
sleep(0.5)

oled_text("Press button to start", oled)
bootwait()
oled_text("Starting...", oled)
sleep(1)
oled_text("Working", oled)

v_c = ir_c.read_u16()
fin = v_c > 4000

while fin == False:  # while robot is not over finish zone:
    # read sensor values for IR and ultrasonic sensor
    v_c = ir_c.read_u16()
    fin = v_c > 4000
    dist = ultrasonic.distance_mm()

    if dist > 200:
        angle(180, servo)
        sleep(0.5)
        motor_left.set_forwards()
        motor_right.set_forwards()
        motor_left.duty(pwm["l_40"])
        motor_right.duty(pwm["r_40"])
        while True:
            for a in range(180, 19, -10):
                angle(a, servo)
                sleep(0.25)
                dist = ultrasonic.distance_mm()
                ang = a
                if dist < 200:
                    stop = True
                    break
            if stop == True:
                stop = False
                break
            for a in range(20, 181, 10):
                angle(a, servo)
                sleep(0.25)
                dist = ultrasonic.distance_mm()
                ang = a
                if dist < 200:
                    stop = True
                    break
            if stop == True:
                stop = False
                break
        motor_left.duty(0)
        motor_right.duty(0)
        print(ang)
    else:
        ang = 90


    if ang < 90:
        wall = "right"
        angle(20, servo)
        sleep(1)
        dist = ultrasonic.distance_mm()
        while dist > 200:
            motor_right.set_forwards()
            motor_right.duty(pwm["r_40"])
            sleep(0.1)
            print("wall 0")
            dist = ultrasonic.distance_mm()



    elif ang > 90:
        wall = "left"
        angle(180, servo)
        sleep(1)
        dist = ultrasonic.distance_mm()
        while dist > 200:
            motor_left.set_forwards()
            motor_left.duty(pwm["l_40"])
            sleep(0.1)
            print("wall 180")
            dist = ultrasonic.distance_mm()

    motor_left.duty(0)
    motor_right.duty(0)
    sleep(1)


    if wall == "right":
        motor_left.set_forwards()
        motor_right.set_forwards()
        motor_left.duty(pwm["l_50"])
        motor_right.duty(pwm["r_50"])
        while fin == False:
            v_c = ir_c.read_u16()
            fin = v_c > 4000
            dist = ultrasonic.distance_mm()
            if dist > 200:
                motor_left.duty(0)
                motor_right.set_backwards()
                motor_right.duty(pwm["r_40"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)
            elif dist < 100:
                motor_right.duty(0)
                motor_left.set_backwards
                motor_left.duty(pwm["l_40"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)
            else:
                motor_left.set_forwards()
                motor_right.set_forwards()
                motor_left.duty(pwm["l_50"])
                motor_right.duty(pwm["r_50"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)

    if wall == "left":
        motor_left.set_forwards()
        motor_right.set_forwards()
        motor_left.duty(pwm["l_50"])
        motor_right.duty(pwm["r_50"])
        while fin == False:
            v_c = ir_c.read_u16()
            fin = v_c > 4000
            dist = ultrasonic.distance_mm()
            if dist > 200:
                motor_right.duty(0)
                motor_left.set_backwards()
                motor_left.duty(pwm["l_40"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)
            elif dist > 100:
                motor_left.duty(0)
                motor_right.set_backwards()
                motor_right.duty(pwm["r_40"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)
            else:
                motor_left.set_forwards()
                motor_right.set_forwards()
                motor_left.duty(pwm["l_50"])
                motor_right.duty(pwm["r_50"])
                sleep(0.2)
                motor_left.duty(0)
                motor_right.duty(0)
                sleep(0.3)
            


motor_left.duty(0)
motor_right.duty(0)
oled_text("Goal Complete!", oled)
LED.on()



