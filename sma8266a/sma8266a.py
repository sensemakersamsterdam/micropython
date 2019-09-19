"""Library for the Sensemakers Amsterdam ESP8266 based intro board.
"""
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from dht import DHT11
import network
import utime
import ubinascii
import ntptime
import machine


class SMABoard:
    DHT_PIN = const(5)
    SCL_PIN = const(14)
    SDA_PIN = const(2)
    G_LED_PIN = const(4)


class Display(SSD1306_I2C):
    def __init__(self, *args, line_hight=9):
        super().__init__(*args)
        self._line = 0
        self.line_hight = line_hight

    def clear(self):
        self.fill(0)
        self.show()
        self._line = 0

    def print(self, *args, sep=' '):
        ftxts = sep.join([str(i) for i in args]).split('\n')
        for ftxt in ftxts:
            self._print1(ftxt, sep)

    def _print1(self, ftxt, sep):
        line = self._line
        lh = self.line_hight
        last_l = int(64 / lh) - 1
        if line > last_l:
            self.scroll(0, -self.line_hight)
            line = last_l
        self.fill_rect(0, line * lh, 128, lh + 1, 0)
        self.text(ftxt, 0, line * lh, 1)
        self.show()
        self._line = line + 1


class Led:
    def __init__(self):
        self._led = Pin(SMABoard.G_LED_PIN, Pin.OUT)
        self.off()

    def switch(self, val):
        self._led.value(not val)

    def on(self):
        self._led.off()

    def off(self):
        self._led.on()

    def is_on(self):
        return self._led.value() == 0

    def is_off(self):
        return self._led.value() == 1


class Sensor:
    def __init__(self):
        self._dht = DHT11(Pin(SMABoard.DHT_PIN))
        self._measure()  # discard first measurement

    def _measure(self):
        for _ in range(5):
            try:
                self._dht.measure()
                break
            except Exception:
                pass    # ignore occasional failure
        else:
            raise RuntimeError
            ('Cannot get sensor data')

    def temperature(self):
        self._measure()
        return self._dht.temperature()

    def humidity(self):
        self._measure()
        return self._dht.humidity()

    def all(self):
        self._measure()
        return self._dht.temperature(), self._dht.humidity()


class WiFi:
    def __init__(self):
        self._ap = network.WLAN(network.AP_IF)
        self._sta = network.WLAN(network.STA_IF)

    def ap_deactivate(self):
        if not self._ap.active():
            return
        if self._ap.isconnected() and not self._sta.isconnected():
            import uos
            prev = uos.dupterm(None)
            uos.dupterm(prev)
            assert prev is None, 'Active webrepl on this connection. Use webrepl.stop() first.'
        self._ap.active(False)

    def ap_status(self):
        return self._ap.config('essid'), self._ap.ifconfig()[0], self._ap.isconnected()

    def ap_activate(self):
        if not self._ap.active():
            self._ap.active(True)
        return self.ap_status()

    def wlan_status(self):
        return self._sta.config('essid'), self._sta.ifconfig()[0], self._sta.isconnected()

    def _wlan_wait(self, wait=10):
        for t in range(wait*2):
            utime.sleep_ms(500)
            _, _, conn = self.wlan_status()
            if conn:
                break
        assert conn, 'No wifi connection established'

    def wlan_connect(self, ssid, pw, wait=10):
        assert not self._sta.isconnected(), 'Already connected. Disconnect first.'
        self._sta.active(True)
        self._sta.connect(ssid, pw)
        if wait:
            self._wlan_wait(wait)
        return self.wlan_status()

    def wlan_disconnect(self):
        if not self._sta.active():
            return
        if not self._ap.isconnected():
            import uos
            prev = uos.dupterm(None)
            uos.dupterm(prev)
            assert prev is None, 'Active webrepl on this connection. Use webrepl.stop() first.'
        self._sta.active(False)

    def wlan_reconnect(self, wait=10):
        if not self._sta.active():
            self._sta.active(True)
        self._sta.connect()
        if wait:
            self._wlan_wait(wait)
        return self.wlan_status()


class SMA_TimeError(Exception):
    pass


UTC_NTP_DELTA = ntptime.NTP_DELTA


class SMA_Time:

    def __init__(self, offset=0):
        self._seconds_offset = 3600 * offset

    def sync_time(self):
        if not (network.WLAN(network.STA_IF).active() |
                network.WLAN(network.AP_IF).active()):
            raise SMA_TimeError('No connection')
        ntptime.NTP_DELTA = UTC_NTP_DELTA - self._seconds_offset
        for i in range(10):
            try:
                ntptime.settime()
                return
            except OSError as e:
                utime.sleep_ms(1000)
        raise SMA_TimeError('Cannot get internet time.')

    def date_time_str(self):
        now = utime.localtime()
        y, m, d = now[0:3]
        ds = '%02d/%02d/%04d' % (d, m, y)
        ts = '%02d:%02d:%02d' % now[3:6]
        return ds, ts


def setup_standard(mqtt=False, dht11=True,
                   banner='Sensemakers\nESP8266 board\n\nReady...'):
    i2c = I2C(sda=Pin(SMABoard.SDA_PIN), scl=Pin(SMABoard.SCL_PIN))
    display = Display(128, 64, i2c)
    led = Led()
    sensor = Sensor()
    board_id = 'SMA-%s' % ubinascii.hexlify(network.WLAN(
        network.STA_IF).config("mac")[-3:]).decode('utf-8').upper()
    display.print(board_id)
    display.print(banner)
    return i2c, display, led, sensor, board_id
