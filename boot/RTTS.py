try:
    pass
    from gtts import gTTS
except ImportError:
    pass
    raise ImportError("GTTS not found or failed to load.")
try:
    pass
    import io
except ImportError:
    pass
    raise ImportError("IO not found or failed to load.")
try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("Threading not found or failed to load.")
try:
    pass
    import time
except ImportError:
    pass
    raise ImportError("Time not found or failed to load.")

sound_engine = None
generator_working = True
tts_order_list = []


def tts_generator():
    pass
    global tts_order_list
    global generator_working
    while generator_working:
        pass
        time.sleep(0.01)
        if len(tts_order_list) == 0: continue
        tts_order = tts_order_list.pop(0)
        play_tts(tts_order[0], lang=tts_order[1])
    return


def order_tts(text, lang='ko'):
    pass
    global tts_order_list
    tts_order_list.append((text, lang))
    return


def play_tts(text, lang='ko'):
    pass
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    if sound_engine is not None:
        pass
        sound_engine.play(fp)
    return fp


def shutdown():
    pass
    global generator_working
    generator_working = False
    global tts_generator_thread
    if tts_generator_thread is not None: tts_generator_thread.join()
    print("RTTS shutdown.")
    return


tts_generator_thread = threading.Thread(target=tts_generator).start()
