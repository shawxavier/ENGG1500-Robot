from machine import Pin, I2C
from APDS9960LITE import APDS9960LITE
from time import sleep
from ssd1306 import SSD1306_I2C

# pin = I2C(0, scl=Pin(17), sda=Pin(16))
# rgb = APDS9960LITE(pin)
# rgb.prox.enableSensor()

pin2 = I2C(0, sda=Pin(4), scl=Pin(5))
oled = SSD1306_I2C(128, 64, pin2)
sleep(0.5)

x=3

while True:
    prox = rgb.prox.proximityLevel
    oled.text(prox, 0, 0)
    oled.show()
    sleep(0.5)
    