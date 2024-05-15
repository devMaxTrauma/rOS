class SoundEngine:
    import pygame
    import threading

    channels = []

    def __init__(self):
        self.pygame.init()
        self.threading.Thread(target=self._running).start()

    def _running(self):
        while True:
            for channel in self.channels:
                if not channel.get_busy():
                    self.channels.remove(channel)
            self.pygame.time.Clock().tick(10)
            if not self.channels:
                break

    def play(self, sound_path):
        channel = self.pygame.mixer.Channel(len(self.channels))
        sound = self.pygame.mixer.Sound(sound_path)
        channel.play(sound)
        self.channels.append(channel)
        if self.threading.active_count() == 1:
            self.threading.Thread(target=self._running).start()
        return channel

    def stop(self, channel):
        channel.stop()
        self.channels.remove(channel)


sound_engine = SoundEngine()
# sound_engine.play("MK3.wav")
channel1 = sound_engine.play("startup.wav")
#
# import time
# time.sleep(4)
# channel2 = sound_engine.play("startup.wav")
# time.sleep(2)

# sound_engine.play("macStartup.mp3")
