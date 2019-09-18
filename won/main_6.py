from sma8266a import *
from won import *
from time import sleep

i2c, display, led, sensor, board_id = setup_standard()

display.clear()
display.print('Connecting...')

wifi_connect()
ip = wifi_ip()

if ip:
    display.print('My IP and board:')
    display.print(ip, '\n', board_id)
else:
    display.print('Not connected.')
    display.print('Reset plse!')
    while True:
        pass  # Hang forever

sma = SMA_Backend(board_id)

while True:
    sma.send(temp=sensor.temperature(), hum=sensor.humidity())
    sleep(30)
