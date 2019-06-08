# Import Eclipse Pahg MQTT module
import paho.mqtt.client as mqtt
# Import Bridge Module
import bridge


class MQTTController():

    def __init__(self):
        self.client = mqtt.Client("RPi Hub")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if int(rc) == 0:
            print("Connected to MQTT broker.")
            bridge.mqttClientConnected = True
            self.subscribeToTopics()

        else:
            print("Failed to connect to MQTT broker.")

    def on_disconnect(self, client, userdata, rc):
        if int(rc) == 0:
            print("Disconnected from MQTT broker.")
            bridge.mqttClientConnected = False
            bridge.mqttClientDisconnected = True
        else:
            print("Lost connection to MQTT broker.")

    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        topic = str(message.topic)

        # Bluetooth Pairing Message Received
        if topic == "Bluetooth-Pair":
            if payload == "1":
                bridge.mqttBluetoothPair = True
        # RPi Hub Remote Message Received
        elif topic == "RPi-Remote":
            # RPi Hub Remote connected
            if payload == "0":
                bridge.audioController.playSystemAudio(50)
        # System Update Message Received
        elif topic == "OS-Update":
            if payload == "0":
                bridge.audioController.playSystemAudio(5)
        else:
            bridge.audioController.playSystemAudio(4)

    def subscribeToTopics(self):
        self.client.subscribe("Bluetooth-Pair")
        self.client.subscribe("RPi-Remote")
        self.client.subscribe("OS-Update")
        self.client.subscribe(".")

    def start(self):
        try:
            self.client.connect("192.168.0.21", 1883)
            self.client.loop_start()
        except:
            return 1
        return 0

    def stop(self):
        self.client.loop_stop()
