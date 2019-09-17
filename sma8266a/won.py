from sma8266a import *
from wifi_credentials import *

wifi = WiFi()


def wifi_connect():
    try:
        wifi.wlan_connect(my_ssid, my_password)
    except:
        pass


def is_wifi_connected():
    return wifi.wlan_status()[2]


def wifi_ip():
    if is_wifi_connected():
        return wifi.wlan_status()[1]
    else:
        return None

