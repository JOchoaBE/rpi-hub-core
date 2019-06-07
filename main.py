# Import GPIO controller module
import pigpio as gpio
# Import DBUS Linux modules
import dbus
import dbus.service
import dbus.mainloop.glib
# Import Threading module
import threading
# Import Signal module
import signal
# Import Time module
import time
# Import System module
import sys
# Import Subprocess module
import subprocess
# Import low level Gnome libraries
from gi.repository import GObject, GLib
# Import Bridge Module
import bridge


# LED Setup Function
def ledSetup():
    gpioController.set_mode(13, gpio.OUTPUT)
    gpioController.write(13, 0)


# Button Setup Function
def buttonSetup():
    gpioController.set_mode(16, gpio.INPUT)
    gpioController.set_mode(26, gpio.OUTPUT)
    gpioController.write(26, 1)


# LED Controller Function
def ledController():
    while True:
        if bridge.pairBlinkLED:
            gpioController.write(13, 1)
            time.sleep(0.3)
            gpioController.write(13, 0)
            time.sleep(0.3)
        elif bridge.pairedBlinkLED:
            gpioController.write(13, 1)
            time.sleep(0.15)
            gpioController.write(13, 0)
            time.sleep(0.15)
            gpioController.write(13, 1)
            time.sleep(0.15)
            gpioController.write(13, 0)
            time.sleep(1)
        elif bridge.noBlinkLED:
            gpioController.write(13, 0)


# Button Controller Function
def buttonController():
    while True:
        # Bluetooth Start Pairing Button
        if gpioController.read(16):
            if bridge.bluetoothDeviceConnected:
                pass
            else:
                if not bridge.bluetoothInitiateDiscovery:
                    if not bridge.bluetoothHCIDBUSProperties.Get("org.bluez.Adapter1", "Powered"):
                        bridge.bluetoothHCIDBUSProperties.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))
                        print("RPi Hub Bluetooth module powered on.")
                        time.sleep(0.1)
                    bridge.bluetoothHCIDBUSProperties.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(1))
                    print("RPi Hub is now discoverable.")

                    # Play Bluetooth device pairing announcement
                    bridge.audioController.playSystemAudio(1)

                    # Change LED status to pairing
                    bridge.pairBlinkLED = True

                    bridge.bluetoothInitiateDiscovery = True
                    time.sleep(0.3)
                elif bridge.bluetoothInitiateDiscovery:
                    bridge.bluetoothHCIDBUSProperties.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(0))
                    print("RPi Hub no longer discoverable.")
                    bridge.pairBlinkLED = False
                    bridge.bluetoothInitiateDiscovery = False
                    time.sleep(0.3)


# Application Interrupt Handler Function
def appInterrupt(x, y):
    print("RPi Hub Core interrupted. Quitting...")
    dbusLoop.quit()
    gpioController.stop()
    subprocess.call('killall pulseaudio', shell=True)
    time.sleep(0.5)
    sys.exit(0)

# Defines this module as the MAIN module
if __name__ == "__main__":

    try:
        # Command Line User Interface
        print("")
        print("RPi Hub - CLI")
        print("==================")

        # Capture external application interrupt
        signal.signal(signal.SIGINT, appInterrupt)

        # Initialize GPIO controller
        gpioController = gpio.pi()

        # Initialize GPIO components
        buttonSetup()
        ledSetup()

        # Run Button Controller function in new thread
        threadButton = threading.Thread(target=buttonController)
        threadButton.start()

        # Run LED Controller function in new thread
        threadLED = threading.Thread(target=ledController)
        threadLED.start()

        # Start PulseAudio sound server
        print("Starting PulseAudio sound server...")
        subprocess.call('killall pulseaudio', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        subprocess.call('pulseaudio --start', shell=True)
        time.sleep(0.5)

        # Set default startup volume
        subprocess.call('pactl set-sink-volume 0 35%', shell=True)

        # Run DBUS asynchronous event loop in new thread
        #dbusLoop = GLib.MainLoop()
        dbusLoop = GObject.MainLoop.new(None, False)
        threadDBUS = threading.Thread(target=dbusLoop.run)
        threadDBUS.start()

        # Start MQTT broker
        print("Starting MQTT broker...")
        subprocess.run(['killall', 'mosquitto'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        subprocess.run(['/usr/local/sbin/mosquitto', '-d'])
        time.sleep(0.5)

        # Start MQTT client
        print("Connecting to MQTT broker...")
        threadMQTT = threading.Thread(target=bridge.mqttController.connect)

        print("RPi Hub Core boot successful.")

    except KeyboardInterrupt:
        #print("Quitting DBUS protocol access...")
        #dbusLoop.quit()
        #print("Quitting GPIO controller...")
        #gpioController.stop()
        #print("Quitting PulseAudio sound server...")
        #subprocess.call('killall pulseaudio', shell=True)
        #time.sleep(0.5)
        sys.exit(0)













