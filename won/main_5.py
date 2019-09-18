from sma8266a import *
from won import *
from time import sleep

i2c, display, led, sensor, board_id = setup_standard()

display.clear()
display.print('Connecting...')

wifi_connect()
ip = wifi_ip()

if ip:
    display.print('My IP address:')
    display.print(ip)
else:
    display.print('Not connected.')
    display.print('Reset plse!')
    while True:
        pass  # Hang forever
