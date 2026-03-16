from xinitialise import initialise
ir_l, ir_c, ir_r, left, right, ultrasonic, servo, enc, LED = initialise()
from time import sleep

pwm=[30, 50, 80, 100]

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
    
    print(l)
    print(r)
    
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
