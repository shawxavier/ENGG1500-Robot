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

print("Press button to start")
bootwait()
print("Starting...")
sleep(1)

while True:
    v_c = ir_c.read_u16()
    fin = v_c > 4000
    
    
    while fin == False: # while robot is not over finish zone:
        # read sensor values for IR and ultrasonic sensor
        v_c = ir_c.read_u16()
        fin = v_c > 4000
        dist = ultrasonic.distance_mm()
        
        # Start if statements
        if dist > 200: # If dist is greater than 200:
            print("Drive")
            # Go forwards, slowly
            motor_left.set_forwards()
            motor_right.set_forwards()
            motor_left.duty(pwm["l_30"])
            motor_right.duty(pwm["r_30"])
            
        elif dist < 200 and dist > 100: # else, if dist is between 200 and 100:
            print("Turn")
            # stop and wait
            motor_left.duty(0)
            motor_right.duty(0)
            sleep(0.5)
            # Spin on spot for 0.2s
            motor_left.set_backwards()
            motor_left.duty(pwm["l_30"])
            motor_right.duty(pwm["r_30"])
            sleep(0.2)
            
        elif dist < 100: #else, if distance is too close (somehow):
            print("Back and Turn")
            # Stop and wait
            motor_left.duty(0)
            motor_right.duty(0)
            sleep(0.5)
            #  Go backwards for 0.5s
            motor_left.set_backwards()
            motor_right.set_backwards()
            motor_left.duty(pwm["l_30"])
            motor_right.duty(pwm["r_30"])
            sleep(0.5)
            # Spin on spot for 0.2s
            motor_right.set_forwards()
            sleep(0.2)
            
        sleep(0.1)
        
    motor_left.duty(0)
    motor_right.duty(0)
    print("Goal Complete!")
    LED.on()
    
    break

