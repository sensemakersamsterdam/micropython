from sma8266a import *
from credentials import *
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


class MQTT_Backend:
    def __init__(self, sensor_id, topic='test', template='{"payload":%s}', cb=None):
        self._sensor_id = sensor_id
        self._mqtt_client = MQTTClient(sensor_id, my_mqtt_host,
                                       port=my_mqtt_port,
                                       user=my_mqtt_user,
                                       password=my_mqtt_password)
        self._topic = topic
        self._template = template
        if cb is not None:
            self._mqtt_client.set_callback(cb)
            self._mqtt_client.connect()
            self._mqtt_client.subscribe(topic)
        else:
            self._mqtt_client.connect()

    def send(self, **params):
        print(self._template % json.dumps(params))
        self._mqtt_client.publish(
            self._topic, self._template % json.dumps(params))

    def poll(self):
        self._mqtt_client.check_msg()
