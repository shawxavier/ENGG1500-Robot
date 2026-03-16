""" This is code that prints the sensor readings to the REPL when the boot button is pressed"""
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

#initialises l c r values
l = 0
c = 0
r = 0

while True:
    w_l = ir_l.read_u16()
    w_c = ir_c.read_u16()
    w_r = ir_r.read_u16()
    
    if boot():
        if w_l > l:
            l = w_l
        if w_c > c:
            c = w_c
        if w_r > r:
            r = w_r
        
        print(f"left: {l}")
        print(f"centre: {c}")
        print(f"right: {r}\n")
        sleep(0.1)
    else:
        l = 0
        r = 0
        c = 0
    sleep(0.1)
