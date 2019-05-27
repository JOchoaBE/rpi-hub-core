# This module is used as a bridge that defines global variables, functions, as well as global DBUS functionality

### IMPORT STATEMENTS ###
# Import Subprocess module
import subprocess
# Import OS module
import os
# Import Audio Controller Module
from audio import audiocontroller

# Import DBUS Linux modules
import dbus.mainloop.glib
# Import Bluetooth Agent
from bluetooth import bluetoothagent


### GLOBAL VARIABLES ###

# Instantiate Audio Controller Class
audioController = audiocontroller.AudioController()

# LED Variables
pairBlinkLED = False
pairedBlinkLED = False
noBlinkLED = False

# Bluetooth Variables
bluetoothInitiateDiscovery = False
bluetoothDeviceConnected = False
connectedBluetoothDeviceName = ""

### DBUS ###


# Find connected Bluetooth device in DBUS
def defineBluetoothDevice(deviceAddress):
    global bluetoothDeviceDBUS
    global bluetoothDeviceDBUSProperties
    global bluetoothDeviceDBUSPropertiesChangedSignal
    bluetoothDeviceDBUS = systemBus.get_object("org.bluez", deviceAddress)
    bluetoothDeviceDBUSProperties = dbus.Interface(bluetoothDeviceDBUS, "org.freedesktop.DBus.Properties")
    bluetoothDeviceDBUSPropertiesChangedSignal = bluetoothDeviceDBUSProperties.connect_to_signal("PropertiesChanged", monitorBluetoothDeviceStatus)


# Monitor connected Bluetooth device status
def monitorBluetoothDeviceStatus(interface, dictionary, var3):
    global pairedBlinkLED
    global noBlinkLED
    global connectedBluetoothDeviceName
    global bluetoothDeviceConnected
    if interface == "org.bluez.Device1":
        if "Connected" in dictionary and dictionary["Connected"] == 0:
            if bluetoothDeviceConnected:
                print("Bluetooth device %s disconnected." % (connectedBluetoothDeviceName))
                bluetoothDeviceConnected = False

                # Play Bluetooth device disconnected announcement
                audioController.playSystemAudio(3)

                # Change LED status to disconnected
                pairedBlinkLED = False
                noBlinkLED = True
            else:
                return
    else:
        return


# Set as DBUS default main loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Initialize DBUS System Bus
systemBus = dbus.SystemBus()

# Initialize DBUS Bluetooth Protocol
bluetoothDBUS = systemBus.get_object("org.bluez", "/org/bluez")
bluetoothHCIDBUS = systemBus.get_object("org.bluez", "/org/bluez/hci0")
bluetoothDeviceDBUS = None
bluetoothAdapter = dbus.Interface(bluetoothHCIDBUS, "org.bluez.Adapter1")
bluetoothAgent = dbus.Interface(bluetoothDBUS, "org.bluez.AgentManager1")

# Define DBUS Bluetooth Property methods
bluetoothHCIDBUSProperties = dbus.Interface(bluetoothHCIDBUS, "org.freedesktop.DBus.Properties")
bluetoothDeviceDBUSProperties = None

# Define DBUS Bluetooth Device Properties Changed Signal
bluetoothDeviceDBUSPropertiesChangedSignal = None
#bluetoothHCIDBUSPropertiesChangedSignal = bluetoothHCIDBUSProperties.connect_to_signal("PropertiesChanged", someHandler)

# Define DBUS Bluetooth Introspect methods
bluetoothHCIDBUSIntrospect = dbus.Interface(bluetoothHCIDBUS, "org.freedesktop.DBus.Introspectable")

# Register Bluetooth Agent
bluetoothObjectPath = "/rpi_hub_core/bluetooth"
bluetoothAgentObject = bluetoothagent.BluetoothAgent(systemBus, bluetoothObjectPath)
bluetoothAgent.RegisterAgent(bluetoothObjectPath, "NoInputNoOutput")
bluetoothAgent.RequestDefaultAgent(bluetoothObjectPath)


### GLOBAL FUNCTIONS ###


