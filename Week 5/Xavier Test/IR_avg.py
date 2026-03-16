"""This code takes 64 samples from each sensor, averages them, and prints the result.
To help with the occasional imperfections in the line quality."""
from machine import Pin, ADC #imports requirements for IR sensors
from motor import Motor
from rp2 import bootsel_button as boot
from time import sleep
import utime

"""#don't worry about this- a silly first attempt at defining the average command... more would need to happen here.
    def avg(l, c, r):
    
    #initialise averages and counts to 0
    sum_l= 0
    sum_c = 0
    sum_r = 0
    count_l = 0
    count_c = 0
    count_r = 0
    
    # take 64 samples of the ground and sum them up (also counting how many samples taken)
    for i in range (1,65):
        if l < 50000: # range given in case of false read (over a void)
            sum_l += l
            count_l += 1
        if c < 50000:
            sum_c += c
            count_c += 1
        if r < 50000:
            sum_r += r
            count_r += 1
            
    if count_l = 0 or count_c = 0 or count_r = 0: #if the code took no samples:
        print("Error!")
    else: #otherwise, take the average of the sum
        avg_l = sum_1 / count_l
        avg_c = sum_c / count_c
        avg_r = sum_r / count_r
    return avg_l, avg_c, avg_r"""

#set IR inputs as analogue
ir_l = ADC(Pin(26))
ir_c = ADC(Pin(27))
ir_r = ADC(Pin(28))

sum_l= 0
sum_c = 0
sum_r = 0
count_l = 0
count_c = 0
count_r = 0

while True:
    
    if boot():
        # take 64 samples of the ground and sum them up (also counting how many samples taken)
        
        for i in range (1,65):
            
            v_l = ir_l.read_u16()
            v_c = ir_c.read_u16()
            v_r = ir_r.read_u16()
        
            if v_l < 50000: # range given in case of false read (over a void)
                sum_l += v_l
                count_l += 1
            if v_c < 50000:
                sum_c += v_c
                count_c += 1
            if v_r < 50000:
                sum_r += v_r
                count_r += 1
                
        if (count_l == 0) or (count_c == 0) or (count_r == 0): #if the code took no samples:
            print("Error!")
             
        else: #otherwise, take the average of the sum
            avg_l = int(sum_l / count_l)
            avg_c = int(sum_c / count_c)
            avg_r = int(sum_r / count_r)
         
            #print averages
            print("Left", avg_l, "Centre", avg_c, "Right", avg_r)
        
        sum_l= 0
        sum_c = 0
        sum_r = 0
        count_l = 0
        count_c = 0
        count_r = 0
            
        sleep(0.1)
    
    
    
        