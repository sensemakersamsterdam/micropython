from sma8266a import *
from wifi_credentials import *
from mqtt.robust import MQTTClient
import ubinascii
import json

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


class SMA_Backend:
    def __init__(self, sensor_id):
        self._sensor_id = sensor_id
        self._mqtt_client = MQTTClient(sensor_id, 'mqtt.sensemakersams.org',
                                       port=9998, user='WON', password='won1234')
        self._mqtt_client.connect()
        self._topic = 'pipeline/WON/' + sensor_id
        self._template = '{"app_id":"WON", "dev_id": "' + \
            sensor_id + '", "payload_fields": %s}'

    def send(self, **params):
        self._mqtt_client.publish(
            self._topic, self._template % json.dumps(params))
