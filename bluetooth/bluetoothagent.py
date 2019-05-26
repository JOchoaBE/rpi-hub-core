# Import DBUS Service Linux module
import dbus.service
# Import Threading module
import threading
# Import Bridge Module
import bridge


# Bluetooth Agent Class
class BluetoothAgent(dbus.service.Object):

    # Set pin code for Bluetooth pairing
    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        return "5742"

    # Authorize Bluetooth pairing
    @dbus.service.method("org.bluez.Agent1", in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):

        thread = threading.Thread(target=registerBluetoothDevice, args=(device,))
        thread.start()
        return


# Register connected Bluetooth device to database
def registerBluetoothDevice(device):
    deviceFullAddress = str(device)
    deviceMacAddressUgly = deviceFullAddress.replace("/org/bluez/hci0/dev_", "")
    deviceMacAddress = deviceMacAddressUgly.replace("_", ":")
    deviceMacAddressMatch = False

    if not bridge.bluetoothDeviceConnected:
        with open("bluetoothDevices.txt", 'a+') as bluetoothDeviceFile:
            bluetoothDeviceFile.seek(0)
            data = bluetoothDeviceFile.readlines()

            for line in data:
                if deviceFullAddress in line:
                    print("This Bluetooth device has already been registered to the RPi Hub Bluetooth database.")
                    deviceMacAddressMatch = True
                    break

            if not deviceMacAddressMatch:
                bluetoothDeviceFile.seek(0, 2)
                bluetoothDeviceFile.write(deviceFullAddress + '\n')
                print("Bluetooth device %s successfully registered to the RPi Hub Bluetooth database." % (deviceMacAddress))

        print("Bluetooth device %s connected." % (deviceMacAddress))

        # Play Bluetooth device connected announcement
        bridge.audioController.playSystemAudio(2)

        bridge.bluetoothInitiateDiscovery = False
        bridge.bluetoothDeviceConnected = True
        bridge.connectedBluetoothDeviceName = deviceMacAddress

        # Change LED status to connected
        bridge.pairBlinkLED = False
        bridge.pairedBlinkLED = True

        # Turn off Bluetooth discovery
        bridge.bluetoothHCIDBUSProperties.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(0))
        print("RPi Hub no longer discoverable.")
        # Monitor connected Bluetooth device
        bridge.defineBluetoothDevice(deviceFullAddress)
    else:
        return
