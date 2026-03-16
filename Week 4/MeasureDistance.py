import time
from ultrasonic import sonic
from motor import Motor
print("Hello, world!")  # Print a welcome message on reset

# These statements make the code more readable.
# Instead of a pin number 2 or 3 we can now write "TRIG" or "ECHO"
TRIG = 3
ECHO = 2
ultrasonic_sensor = sonic(TRIG, ECHO)
motor_left = Motor("left", 8, 9, 6)
motor_left.set_forwards()
while True:
    dist = ultrasonic_sensor.distance_mm()
    if dist < 200:
        # The code within this if-statement only gets executed
        # if the distance measured is less than 200 mm
        print("Distance = {:6.2f} [mm]".format(dist))
        motor_left.duty(0)
    else:
        motor_left.duty(50)
    time.sleep(0.1)