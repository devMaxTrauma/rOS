class Sound:
    sounding_thread = None
    thread_manager = None
    pygame_manager = None
    sound = None

    def __init__(self, sound_path):
        import threading
        import pygame
        self.sound = sound_path
        self.thread_manager = threading
        self.pygame_manager = pygame

    def play(self):
        self.sounding_thread = self.thread_manager.Thread(target=self.play_sound)
        self.sounding_thread.start()

    def play_sound(self):
        self.pygame_manager.mixer.init()
        self.pygame_manager.mixer.music.load(self.sound)
        self.pygame_manager.mixer.music.play()
        while self.pygame_manager.mixer.music.get_busy():
            self.pygame_manager.time.Clock().tick(10)

    def stop(self):
        self.pygame_manager.mixer.music.stop()
        self.sounding_thread.join()


start1 = Sound("startup.wav")
start2 = Sound("MK3.wav")

start1.play()
import time
time.sleep(0.1)
start2.play()
time.sleep(2)
start1.play()
