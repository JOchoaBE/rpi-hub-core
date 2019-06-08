# Import Operating System Interface module
import os
import time
# Import PyGame Multimedia API
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# Import Threading module
import threading

# Project Root Path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


class AudioController:
    BT_AUDIO_PAIR = os.path.join(ROOT_DIR, "bluetooth/resources/bt_pairing.wav")
    BT_AUDIO_CONNECTED = os.path.join(ROOT_DIR, "bluetooth/resources/bt_connected.wav")
    BT_AUDIO_DISCONNECTED = os.path.join(ROOT_DIR, "bluetooth/resources/bt_disconnected.wav")
    COMMAND_UNKNOWN = os.path.join(ROOT_DIR, "system/resources/command_unknown.wav")
    OS_UPDATE_AVAILABLE = os.path.join(ROOT_DIR, "system/resources/os_update_available.wav")

    RPI_REMOTE_CONNECTED = os.path.join(ROOT_DIR, "remote/resources/rpi_remote_connected.wav")
    audioMixer = pygame.mixer

    def __init__(self):
        pass

    def playSystemAudio(self, option):
        self.audioMixer.init()
        if option == 0:
            pass
        # Bluetooth Ready To Pair Announcement
        elif option == 1:
            announcer = self.audioMixer.Sound(self.BT_AUDIO_PAIR)
            thread = threading.Thread(target=announcer.play)
            thread.start()
        # Bluetooth Device Connected Announcement
        elif option == 2:
            announcer = self.audioMixer.Sound(self.BT_AUDIO_CONNECTED)
            thread = threading.Thread(target=announcer.play)
            thread.start()
        # Bluetooth Device Disconnected Announcement
        elif option == 3:
            announcer = self.audioMixer.Sound(self.BT_AUDIO_DISCONNECTED)
            thread = threading.Thread(target=announcer.play)
            thread.start()
        # Unknown Command Announcement
        elif option == 4:
            announcer = self.audioMixer.Sound(self.COMMAND_UNKNOWN)
            thread = threading.Thread(target=announcer.play)
            thread.start()
        # System Update Available Announcement
        elif option == 5:
            announcer = self.audioMixer.Sound(self.OS_UPDATE_AVAILABLE)
            thread = threading.Thread(target=announcer.play)
            thread.start()
        # RPi Hub Remote Connected Announcement
        elif option == 50:
            announcer = self.audioMixer.Sound(self.RPI_REMOTE_CONNECTED)
            thread = threading.Thread(target=announcer.play)
            thread.start()

        else:
            pass