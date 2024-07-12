try:
    import pygame
except ImportError:
    raise ImportError("Pygame not found. Please install Pygame.")
try:
    import threading
except ImportError:
    raise ImportError("Threading not found. Please install Threading.")

channels = []
running_thread = None


def _check_channel(channel):
    global channels
    if not channel.get_busy(): channels.remove(channel)


def _running():
    while True:
        for channel in channels: _check_channel(channel)
        pygame.time.Clock().tick(10)
        if not channels: break


def play(sound_path, repeat=0):
    global running_thread
    global channels
    channel = pygame.mixer.Channel(len(channels))
    sound = pygame.mixer.Sound(sound_path)
    channel.play(sound, repeat)
    channels.append(channel)
    if running_thread is None or not running_thread.is_alive():
        running_thread = threading.Thread(target=_running).start()
    return channel


def stop(channel):
    global channels
    if not channel in channels: return
    channel.stop()
    channels.remove(channel)


def shutdown():
    pygame.quit()
    try:
        running_thread.join()
    except Exception:
        pass
    print("RSound shutdown.")


pygame.init()
running_thread = threading.Thread(target=_running).start()
