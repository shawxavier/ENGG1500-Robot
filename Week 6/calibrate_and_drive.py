from xinitialise import initialise, bootwait, angle, calibrate
from time import sleep

# Set variables from the initialise script
ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED = initialise()

angle(90, servo)

motor_left.duty(0)
motor_right.duty(0)

print("Press to Calibrate") # calibrate gets the same motor speeds for both motors, and puts them in the pwm dictionary
bootwait()
pwm = calibrate(motor_left, motor_right, enc)
print("Calibration Complete!")

bootwait()
enc.clear_count()

while True:

    while enc.get_left() < 100:
        motor_left.set_forwards()
        motor_right.set_forwards()
        motor_left.duty(pwm["l_50"])
        motor_right.duty(pwm["r_50"])
        
    motor_left.duty(0)
    motor_right.duty(0)
