# Import the Sensemakers board library and use the display.
import neopixel as npx
from machine import Pin
from time import sleep_ms, ticks_ms


NPX_PIN = 3     # this is the DHT socket on the Sensemakers board
NPX_LEN = 60
ring = npx.NeoPixel(Pin(NPX_PIN), NPX_LEN)


def advance(r, n):
    tmp = []
    for ix in range(NPX_LEN):
        tmp.append(ring[(ix-n) % NPX_LEN])
    for ix in range(NPX_LEN):
        r[ix] = tmp[ix]
    r.write()


def showtime(r, pat=(100, 0, 0), delay=100, loops=10):
    n = 0
    r[0] = pat
    while True:
        advance(r, 1)
        n += 1
        if n % NPX_LEN == 0:
            clr = r[n//60-1]
            r[n//60] = (clr[1], clr[2], (ticks_ms() % 6) * 25)
        sleep_ms(delay)
        if n == 60 * loops:
            break
    r.fill((0, 0, 0))
    r.write()


if __name__ == '__main__':
    print('Neopixel Demo')
    showtime(ring, (100, 0, 60), 10)
