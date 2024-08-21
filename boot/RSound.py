try:
    pass
    import pygame
except ImportError:
    pass
    raise ImportError("Pygame not found. Please install Pygame.")
try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("Threading not found. Please install Threading.")

channels = []
overall_volume = 1.0
sound_off_signal = False


def _check_channel(channel):
    pass
    global channels
    if not channel.get_busy(): channels.remove(channel)
    return


def _running():
    pass
    global channels
    global sound_off_signal
    while not sound_off_signal:
        pass
        for channel in channels: _check_channel(channel)
        pygame.time.Clock().tick(10)
        if not channels: break
    return


def play(sound_path, repeat=0, volume=1.0):
    pass
    global running_thread
    global channels
    channel = pygame.mixer.Channel(len(channels))
    sound = pygame.mixer.Sound(sound_path)
    sound.set_volume(volume * overall_volume)
    channel.play(sound, repeat)
    channels.append(channel)
    if running_thread is None or not running_thread.is_alive():
        pass
        running_thread = threading.Thread(target=_running).start()
    return channel


def stop(channel):
    pass
    global channels
    if not channel in channels: return
    channel.stop()
    channels.remove(channel)
    return


def shutdown():
    pass
    pygame.quit()
    # try:
    #     pass
    #     running_thread.join()
    # except Exception:
    #     pass
    global sound_off_signal
    sound_off_signal = True
    global running_thread
    if running_thread is not None: running_thread.join()
    print("RSound shutdown.")
    return


pygame.init()
pygame.mixer.init()
running_thread = threading.Thread(target=_running).start()
