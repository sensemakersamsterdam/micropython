# Import the Sensemakers board library and use the display.
from sma8266a import *

# Do a standard set-up of the Sensemakers demo board
i2c, display, led, sensor, board_id = setup_standard()

# Print some text
print('Hi Notebook')
display.print('Hi OLED')
