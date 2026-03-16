import time
from motor import Motor
from ultrasonic import sonic

motor_left = Motor("left", 8, 9, 6)
motor_right = Motor("right", 10, 11, 7)

ultrasonic_sensor = sonic(3, 2)

while True:
    dist = ultrasonic_sensor.distance_mm()
    if dist > 50 and dist <= 200:
        motor_left.duty(0)
        motor_right.duty(0)
    elif dist < 50:
        motor_left.set_backwards()
        motor_right.set_backwards()
        motor_left.duty(50)
        motor_right.duty(50)
    else:
        motor_left.set_forwards()
        motor_right.set_forwards()
        motor_left.duty(50)
        motor_right.duty(50)
    time.sleep(0.1)