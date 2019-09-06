from sma_8266_board_a import *
from time import sleep


i2c, oled, led, sensor = setup_standard()

n = 1

while True:
    t = sensor.temperature()
    h = sensor.humidity()
    oled.clear()
    oled.print('Sensemakers Ams')
    oled.print()
    oled.print('pass: ', n)
    oled.print()
    oled.print('Temperature:', t)
    oled.print('Humidity:', h)
    sleep(10)
    n += 1
