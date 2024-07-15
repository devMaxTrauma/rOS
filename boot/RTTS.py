try:
    from gtts import gTTS
except ImportError:
    raise ImportError("GTTS not found or failed to load.")
try:
    import io
except ImportError:
    raise ImportError("IO not found or failed to load.")
try:
    import threading
except ImportError:
    raise ImportError("Threading not found or failed to load.")
try:
    import time
except ImportError:
    raise ImportError("Time not found or failed to load.")

sound_engine = None
generator_working = True
tts_generator_thread = None
tts_order_list = []


def tts_generator():
    global tts_order_list
    global generator_working
    while generator_working:
        time.sleep(0.01)
        if len(tts_order_list) == 0: continue
        tts_order = tts_order_list.pop(0)
        play_tts(tts_order[0], lang=tts_order[1])


def order_tts(text, lang='ko'):
    global tts_order_list
    tts_order_list.append((text, lang))


def play_tts(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    if sound_engine is not None:
        sound_engine.play(fp)
    return fp


def shutdown():
    try:
        tts_generator_thread.join()
    except Exception:
        pass
    print("RTTS shutdown.")


tts_generator_thread = threading.Thread(target=tts_generator).start()
