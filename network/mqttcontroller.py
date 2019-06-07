# Import Eclipse Pahg MQTT module
import paho.mqtt.client as mqtt
# Import Bridge Module
import bridge


class MQTTController():

    def __init__(self):
        self.client = mqtt.Client("RPi Hub")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if int(rc) == 0:
            print("Connected to MQTT broker.")
            bridge.mqttClientConnected = True
        else:
            print("Failed to connect to MQTT broker.")

    def on_disconnect(self, client, userdata, rc):
        if int(rc) == 0:
            print("Disconnected from MQTT broker.")
            bridge.mqttClientConnected = False
            bridge.mqttClientDisconnected = True
        else:
            print("Lost connection to MQTT broker.")

    def start(self):
        try:
            self.client.connect("192.168.0.21", 1883)
            self.client.loop_start()
        except:
            return 1
        return 0

    def stop(self):
        self.client.loop_stop()
