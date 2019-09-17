# Measure temperature and rel. humidity and put it on the display.

from sma8266a import *
from time import sleep


i2c, display, led, sensor = setup_standard()

display.clear()

t = sensor.temperature()
print('Temperature:', t, 'C')
display.print('Temp', t, 'C')

h = sensor.humidity()
print('Humidity:', h, '%')
display.print('Humidity:', h, '%')