from sma_mqtt import wifi_connect, is_wifi_connected, MQTT_Backend
from time import sleep_ms
from neopixel_demo import showtime, ring
import network
import ubinascii
import json


board_id = 'SMA-%s' % ubinascii.hexlify(network.WLAN(
    network.STA_IF).config("mac")[-3:]).decode('utf-8').upper()

wifi_connect()


def mqtt_msg(topic, msg):
    """Process incoming mqtt message
    """

    topic = topic.decode()
    # The replaces are workaround for iPhone quoting
    msg = msg.decode().replace('“', '"').replace('”', '"')
    print(topic, '->', msg)
    try:
        msg_dict = json.loads(msg)
        print(msg_dict)
        if 'pat' in msg_dict:
            showtime(ring, msg_dict['pat'],
                     delay=msg_dict.get('delay', 5),
                     loops=msg_dict.get('loops', 3))
    except Exception as ex:
        print(ex)
        return


while not is_wifi_connected():
    sleep_ms(1000)
    print('...')

mqtt = MQTT_Backend(board_id, topic='public/workshop', cb=mqtt_msg)

while True:
    mqtt.poll()
    sleep_ms(250)
