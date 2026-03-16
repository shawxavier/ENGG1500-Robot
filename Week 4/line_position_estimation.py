from machine import Pin, ADC
from time import sleep

# ------------------- SENSOR POSITIONS -------------------
# Distances from robot center (mm)
x0 = -15  # left sensor
x1 = 0    # middle sensor
x2 = 15   # right sensor

# ------------------- INITIALIZE ADC -------------------
adc_A0 = ADC(Pin(26))  # left sensor
adc_A1 = ADC(Pin(27))  # middle sensor
adc_A2 = ADC(Pin(28))  # right sensor

# ------------------- SMOOTHING SETUP -------------------
N = 5  # number of readings to average
history = []

# ------------------- MAIN LOOP -------------------
while True:
    # Read raw sensor values
    w0 = adc_A0.read_u16()
    w1 = adc_A1.read_u16()
    w2 = adc_A2.read_u16()

    # Weighted average numerator and denominator
    numerator = (w0 * x0) + (w1 * x1) + (w2 * x2)
    denominator = w0 + w1 + w2

    # Avoid division by zero
    if denominator == 0:
        line_dist = 0
    else:
        line_dist = numerator / denominator

    # Add to history and compute moving average
    history.append(line_dist)
    if len(history) > N:
        history.pop(0)
    smoothed_dist = sum(history) / len(history)

    # Optional: ignore very small fluctuations (noise)
    if abs(smoothed_dist) < 0.05:
        smoothed_dist = 0

    # Print the smoothed line distance in mm
    print("Smoothed Distance from line = {:6.2f} mm".format(smoothed_dist))

    # Small delay for stability
    sleep(0.1)  # 100 ms