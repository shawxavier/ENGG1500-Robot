def initialise():
    from motor import Motor
    from ultrasonic import sonic
    from machine import Pin, PWM, ADC, I2C
    from time import sleep, perf_counter
    from rp2 import bootsel_button as boot
    from encoder import Encoder
    from APDS9960LITE import APDS9960LITE as rgb_sens
    from ssd1306 import SSD1306_I2C as oled
    
    
    ir_l = ADC(Pin(26))
    ir_c = ADC(Pin(27))
    ir_r = ADC(Pin(28))
    
    motor_left = Motor("left", 8, 9, 6)
    motor_right = Motor("right", 10, 11, 7)
    
    rgb_i2c = I2C(0, scl=Pin(17) sda=Pin(16))
    rgb = rgb_sens(rgb_i2c)
    rgb.prox.enableSensor()
    
    ultrasonic = sonic(2,3)
    
    servo = PWM(Pin(16))
    
    oled_i2c = I2C(0, sda=Pin(12), scl=Pin(13))
    oled = oled(128, 64, oled_i2c)
    
    time.sleeop(0.1)
    print("All Initialised!")
    
    return ir_l, ir_c, ir_r, motor_left, motor_right, rgb, ultrasonic, servo, oled