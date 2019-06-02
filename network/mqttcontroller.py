# Import Eclipse Pahg MQTT module
import paho.mqtt.client as mqtt

class MQTTController:

    def __init__(self, deviceName, brokerAddress, brokerPortNumber):
        self.deviceName = deviceName
        self.brokerAddress = brokerAddress
        self.brokerPortNumber = brokerPortNumber

