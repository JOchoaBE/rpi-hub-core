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
    audioMixer = pygame.mixer

    def __init__(self):
        pass

    def playSystemAudio(self, option):
        self.audioMixer.init()
        print(ROOT_DIR)
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
        elif option == 3:
            pass
        elif option == 4:
            pass
        else:
            pass