import pygame
import threading

channels = []


def _running():
    while True:
        for channel in channels:
            if not channel.get_busy():
                channels.remove(channel)
        pygame.time.Clock().tick(10)
        if not channels:
            break


def play(sound_path):
    channel = pygame.mixer.Channel(len(channels))
    sound = pygame.mixer.Sound(sound_path)
    channel.play(sound)
    channels.append(channel)
    if threading.active_count() == 1:
        threading.Thread(target=_running).start()
    return channel


def stop(channel):
    channel.stop()
    channels.remove(channel)


pygame.init()
threading.Thread(target=_running).start()
