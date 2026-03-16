"""This version of initialise is specifically for the competency assessment - It does not have the OLED Display or
    RGB Sensor included, as they fail to initialise if not installed.
    If you're looking for the complete version, use initialise.py
    
    Example in other code:
    from xinitialise import initialise
    ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED = initialise()

    Hopefully that works :)"""

def initialise():
    # Bring in a whole bunch of modules for the robot. As long as the pins are right, this should work...
    from motor import Motor
    from ultrasonic import sonic
    from machine import Pin, PWM, ADC
    from time import sleep
    from encoder import Encoder
    
    # Set IR Pin ins as analogue
    ir_l = ADC(Pin(26))
    ir_c = ADC(Pin(27))
    ir_r = ADC(Pin(28))
    
    # Set motors
    motor_left = Motor("left", 8, 9, 6)
    motor_right = Motor("right", 10, 11, 7)
    
    # Set ultrasonic sensor trig and echo
    ultrasonic = sonic(2,3)
    
    # Set servo motor pwm pin
    servo = PWM(Pin(15))
    servo.freq(50)
    
    # Set encoder
    enc = Encoder(18, 19)
    
    # Set Green LED Indicator
    LED = Pin("LED", Pin.OUT)
    
    # Wait for a moment for it all to turn on
    sleep(0.1)
    print("All Initialised!")
    
    # Send back a list - copy paste this into the top of the other doc
    return ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED

def bootwait():
    # A command that waits for the button to be pressed before running subsequent code
    from rp2 import bootsel_button as boot
    while True:
        if boot():
            break
        
def angle(angle, servo):
    position = int(8000 * ((angle + 7) / 180) + 1000)
    servo.duty_u16(position)

def motor_calibrate(left, right, enc, pwm=[30, 50, 80, 100], time=1):
    
    from motor import Motor
    from encoder import Encoder
    from time import sleep
    
    values = {}
    
    left.set_forwards()
    right.set_forwards()
    
    for i in pwm:
        enc.clear_count()
        left.duty(i)
        right.duty(i)
        
        sleep(time)
        
        l = enc.get_left()
        r = enc.get_right()
        print(l)
        print(r)
        
        if l > r:
            l = round((r / l) * i)
            r = i
            
        elif r > l:
            r = round((l / r) * i)
            l = i
            
        else:
            l = i
            r = i
            
        values[f"l_{i}"] = l
        values[f"r_{i}"] = r
        
        left.duty(0)
        right.duty(0)
        sleep(0.5)
    
    return values
        
def ir_calibrate(l, c, r):
    bootwait()
    w_l = l.read_u16()
    w_c = c.read_u16()
    w_r = r.read_u16()
    bootwait()
    b_l = l.read_u16()
    b_c = c.read_u16()
    b_r = r.read_u16()
    