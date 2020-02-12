import bmp280
from machine import Pin, I2C
from time import sleep

scl=Pin(5)
sda=Pin(4)

i2c=I2C(scl=scl, sda=sda)

print('Found on I2C bus: ', i2c.scan())

bmp=bmp280.BMP280(i2c)

while True:
    print('t=', bmp.temperature, ' p=', bmp.pressure / 100.0)
    sleep(5)
    