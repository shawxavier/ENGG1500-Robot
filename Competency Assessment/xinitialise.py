"""This version of initialise is specifically for the competency assessment - It does not have the OLED Display or
    RGB Sensor included, as they would fail to initialise.
    If you're looking for the complete version, use initialise.py
    
    Example in other code:
    from xinitialise import initial
    ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo = initial()

    Hopefully that works :)"""
def initialise():
    # Bring in a whole bunch of modules for the robot. As long as the pins are right, this should work...
    from motor import Motor
    from ultrasonic import sonic
    from machine import Pin, PWM, ADC
    from time import sleep
    from encoder import Encoder
    
    #Set IR Pin ins as analogue
    ir_l = ADC(Pin(26))
    ir_c = ADC(Pin(27))
    ir_r = ADC(Pin(28))
    
    #set motors
    motor_left = Motor("left", 8, 9, 6)
    motor_right = Motor("right", 10, 11, 7)
    
    #set ultrasonic sensor trig and echo
    ultrasonic = sonic(2,3)
    
    # set servo motor pwm pin
    servo = PWM(Pin(15))
    servo.freq(50)
    
    # set encoder
    enc = Encoder(18, 19)
    
    # Set Green LED Indicator
    LED = Pin("LED", Pin.OUT)
    
    # Wait for a second for it all to turn on
    sleep(0.1)
    print("All Initialised!")
    
    # Send back a list - copy paste this into the top of the other doc
    return ir_l, ir_c, ir_r, motor_left, motor_right, ultrasonic, servo, enc, LED

def bootwait():
    from rp2 import bootsel_button as boot
    while True:
        if boot():
            break
        
def angle(angle, servo):
    position = int(8000 * ((angle + 7) / 180) + 1000)
    servo.duty_u16(position)

def calibrate(left, right, enc, pwm=[30, 50, 80, 100]):
    
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
        
        sleep(1)
        
        l = enc.get_left()
        r = enc.get_right()
        
        if l > r:
            l = int((r / l) * i)
            r = i
            
        elif r > l:
            r = int((l / r) * i)
            l = i
            
        else:
            l = i
            r = i
            
        values[f"l_{i}"] = l
        values[f"r_{i}"] = r
    
    left.duty(0)
    right.duty(0)
    
    return values
        
    