from machine import Pin, ADC #imports requirements for IR sensors
from motor import Motor
from rp2 import bootsel_button as boot
from time import sleep

#set IR inputs as analogue
ir_l = ADC(Pin(26))
ir_c = ADC(Pin(27))
ir_r = ADC(Pin(28))

eps = 20 #small value that matters
    
white_l = 2304 - eps
white_c = 2480 - eps
white_r = 2512 - eps
    
    
black_l = 3424 + eps
black_c = 4897 + eps
black_r = 21029 + eps

    
while True:
    w_l = ir_l.read_u16()
    w_c = ir_c.read_u16()
    w_r = ir_r.read_u16()
    
    count += 1
    
    if boot():
        print(w_l)
        print(w_c)
        print(w_r)
        print()
        
        """norm_l = (w_l - white_l) / (black_l - white_l) * 128
        norm_c = (w_c - white_c) / (black_c - white_c) * 128
        norm_r = (w_r - white_r) / (black_r - white_r) * 128
        print(norm_l)
        print(norm_c)
        print(norm_r)
        print()"""
    sleep(0.01)
    
