from time import sleep
from motor import Motor
from encoder import Encoder

# -------------------------------------------------
# Convert distance (mm) to encoder counts
# d = wheel diameter in mm
# 20 = encoder counts per wheel revolution
# -------------------------------------------------
def dist_to_counts(distance_mm, wheel_diameter=65):
    circumference = wheel_diameter * 3.1459
    return int((distance_mm / circumference) * 20)

# ------------------- PARAMETERS -------------------
# You can easily change these:
distance_forward_mm = 150   # distance to move forward (mm)
distance_backward_mm = 150  # distance to move backward (mm)
base_speed = 35             # 0-100 PWM
Kp = 0.8                    # proportional gain
left_motor_offset = 10      # compensate for slower left motor

# ------------------- CREATE OBJECTS ----------------
motor_left = Motor("left", 8, 9, 6)
motor_right = Motor("right", 10, 11, 7)

ENC_L = 18
ENC_R = 19
enc = Encoder(ENC_L, ENC_R)

# ------------------- HELPER FUNCTIONS -------------
def clamp_pwm(pwm):
    """Clamp PWM to 0-100%"""
    if pwm < 0:
        return 0
    elif pwm > 100:
        return 100
    else:
        return pwm

def move(distance_mm, forwards=True):
    """Drive the robot a certain distance in mm"""
    counts_target = dist_to_counts(distance_mm)
    enc.clear_count()

    if forwards:
        motor_left.set_forwards()
        motor_right.set_forwards()
    else:
        motor_left.set_backwards()
        motor_right.set_backwards()

    while (enc.get_left() + enc.get_right()) / 2 < counts_target:
        left_count = enc.get_left()
        right_count = enc.get_right()
        error = left_count - right_count
        correction = int(Kp * error)

        pwm_left = clamp_pwm(base_speed + left_motor_offset - correction)
        pwm_right = clamp_pwm(base_speed + correction)

        motor_left.duty(pwm_left)
        motor_right.duty(pwm_right)

    # Stop motors at the end
    motor_left.duty(0)
    motor_right.duty(0)
    sleep(0.5)  # brief pause for stability

# ------------------- MAIN LOOP --------------------
try:
    while True:
        # Move forward
        move(distance_forward_mm, forwards=True)

        # Move backward
        move(distance_backward_mm, forwards=False)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    motor_left.duty(0)
    motor_right.duty(0)
    print("Motors safely stopped.")