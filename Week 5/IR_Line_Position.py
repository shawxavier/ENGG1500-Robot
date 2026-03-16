from machine import Pin, ADC #imports requirements for IR sensors
from motor import Motor
from rp2 import bootsel_button as boot
from time import sleep

#set IR inputs as analogue
ir_l = ADC(Pin(26))
ir_c = ADC(Pin(27))
ir_r = ADC(Pin(28))

#set distance from centre of each IR sensor (left is negative direction)
x_l = -15
x_c = 0
x_r = 15

while True:
    w_l = ir_l.read_u16()
    w_c = ir_c.read_u16()
    w_r = ir_r.read_u16()
    
    num = (w_l * x_l) + (w_c * x_c) + (w_r * x_r)
    denom = w_l + w_c + w_r
    
    line_dist = num / denom
    print(f"Distance from line = {line_dist:3.2f}")
    sleep(0.5)