#
# The fully working weather station program..
#

from sma8266a import *
from won import *
from time import sleep, time

# Do the standard board set-up
i2c, display, led, sensor, board_id = setup_standard()

# Erase the display and print progress info
display.clear()
display.print('Connecting...')

# Connect to the WiFi
wifi_connect()

# Get the IP address from the network
ip = wifi_ip()

# Did it work???
if ip:
    # Yes! so display the IP address and the Board ID
    display.print('IP:', ip)
    display.print('ID:', board_id)
else:
    # Nope. Check your credentials and try again...
    display.print('Not connected.')
    display.print('Reset plse!')
    while True:
        pass  # Hang forever

# Assuming the WiFI is on the internet, get the time
# We get GMT, so we specify an offset of 2 hours for
# Central European Summertime. No automatic Summer/Wintertime!
clock = SMA_Time(2)
clock.sync_time()

# Now we connect to the Sensmaker's back end with your board ID.
sma = SMA_Backend(board_id)

led = Led()


while True:     # Repeat the below forever....
    led.on()
    dt, tm = clock.date_time_str()  # Get date and time

    # Display the intro
    display.clear()
    display.print('IP:', ip, sep='')
    display.print('ID:', board_id, sep='')
    display.print('---------------')
    display.print(dt)
    display.print(tm)

    # Get the current temperature and humidity
    try:
        t, h = sensor.all()
        display.print(t, 'C,', h, '%H')
        # Send it to the backend
        sma.send(temp=t, hum=h)
    except Exception:
        display.print('Sensor fail!')
        sma.send(fail=1)

    # and wait some seconds before we do it all again
    led.off()
    sleep(30)
