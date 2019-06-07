# Import Eclipse Pahg MQTT module
import paho.mqtt.client as mqtt
# Import Bridge Module
import bridge


class MQTTController(mqtt.Client):

    def __init__(self, deviceName, brokerAddress, brokerPortNumber):
        self._client_id = deviceName
        #self.deviceName = deviceName
        self.brokerAddress = brokerAddress
        self.brokerPortNumber = brokerPortNumber

    def on_connect(self):
        print("connected")

    def on_message(self):
        pass

    def connect(self):
        self.connect(self.brokerAddress, self.brokerPortNumber)
        self.loop_forever()