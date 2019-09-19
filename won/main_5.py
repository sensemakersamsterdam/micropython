#
# The set-up basics:
#   Setting up all things.
#   Connecting to the internet
#   Getting date and time
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

dt, tm = clock.date_time_str()  # Get date and time
# and display them
display.print(dt)
display.print(tm)
display.print()
display.print('Bye, bye..')
