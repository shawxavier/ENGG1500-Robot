# motor calibration

# ==============================
# Lab 4 - Motor Calibration
# ==============================

from time import sleep
from motor import Motor
from encoder import Encoder


# ----- Pin Definitions -----
# Encoder pins (from your encoder test file)
ENC_L = 18
ENC_R = 19

# Motor pins (from your working files)
motor_left = Motor("left", 8, 9, 6)
motor_right = Motor("right", 10, 11, 7)

# Create encoder object
enc = Encoder(ENC_L, ENC_R)

# Set both motors to forward direction
motor_left.set_forwards()
motor_right.set_forwards()

print("PWM,ENC_L,ENC_R")

# Run calibration once
for pwm in range(0, 101, 5):   # 0 → 100 inclusive, step 5

    # ---- 1. Clear encoder counts ----
    enc.clear_count()

    # ---- 2. Apply PWM to both motors ----
    motor_left.duty(pwm)
    motor_right.duty(pwm)

    # ---- 3. Run motors for 1 second ----
    sleep(1)

    # ---- 4. Read encoder values ----
    left_count = enc.get_left()                           
    right_count = enc.get_right()

    # ---- 5. Print results in CSV format ----
    print("{:3d},{:4d},{:4d}".format(pwm, left_count, right_count))

# ---- Stop motors after test ----
motor_left.duty(0)
motor_right.duty(0)

print("Calibration Complete")