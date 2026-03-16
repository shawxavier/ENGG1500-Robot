"""Code that makes the robot go forward for 0.5 sec when button pressed"""
from motor import Motor
from rp2 import bootsel_button as boot # Imports the bootsel button on the pico as an input
from time import sleep

motor_left = Motor("left", 8, 9, 6)
motor_right = Motor("right", 10, 11, 7)

while True:
    motor_left.set_forwards()
    motor_right.set_forwards()
    if boot(): # When the boot button is pressed
        motor_left.duty(80)
        motor_right.duty(80)
        sleep(0.5)
    motor_left.duty(0)
    motor_right.duty(0)