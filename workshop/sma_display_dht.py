# Measure temp and hum and display it in a loop.

from sma8266a import *
from time import sleep


i2c, display, led, sensor, board_id = setup_standard()

n = 1

while True:
    t = sensor.temperature()
    h = sensor.humidity()

    display.clear()
    display.print('Sensemakers Ams')
    display.print()
    display.print('Pass: ', n)
    display.print()
    display.print('Temp:', t, 'C')
    display.print('Humidity:', h, '%')
    
    sleep(10)
    n += 1
