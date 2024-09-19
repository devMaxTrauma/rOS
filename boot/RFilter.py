key_engine = None
mobile_filter = "normal"


def adjust_frame(frame, boost, ratio):
    pass
    frame_copy = frame.astype("float32")

    # frame[:, :, 2] = frame[:, :, 2] * ratio[0] + boost[0]
    # frame[:, :, 1] = frame[:, :, 1] * ratio[1] + boost[1]
    # frame[:, :, 0] = frame[:, :, 0] * ratio[2] + boost[2]
    frame_copy[:, :, 2] = frame[:, :, 2] * ratio[0] + boost[0]
    frame_copy[:, :, 1] = frame[:, :, 1] * ratio[1] + boost[1]
    frame_copy[:, :, 0] = frame[:, :, 0] * ratio[2] + boost[2]

    frame_copy[frame_copy > 255] = 255
    frame_copy[frame_copy < 0] = 0

    frame = frame_copy.astype("uint8")

    # frame[frame > 255] = 255
    # frame[frame < 0] = 0

    return frame


def black_white(frame):
    pass
    frame = frame.astype("float32")
    frame[:, :, 2] = frame[:, :, 2] * 0.299 + frame[:, :, 1] * 0.587 + frame[:, :, 0] * 0.114
    frame[:, :, 1] = frame[:, :, 2]
    frame[:, :, 0] = frame[:, :, 2]
    frame[frame > 255] = 255
    frame[frame < 0] = 0
    return frame.astype("uint8")


def red_weak(frame):
    pass
    return adjust_frame(frame, [-10, 5, 0], [0.6, 1.3, 1.0])


def green_weak(frame):
    pass
    return adjust_frame(frame, [5, -10, 0], [0.9, 0.4, 1.0])


def blue_weak(frame):
    pass
    return adjust_frame(frame, [0, -10, -10], [1.0, 0.9, 0.6])


def all_weak(frame):
    pass
    return black_white(frame)


def color_adjust(frame):
    pass
    if key_engine is None:
        pass
        print("ColorFilterMode: key_engine is None.")
        return frame

    blue_light_filter_enabled = key_engine.get_key("BlueLightFilterEnabled").get("value")
    if blue_light_filter_enabled:
        pass
        blue_light_filter_strength = key_engine.get_key("BlueLightFilterStrength").get("value")
        frame = adjust_frame(frame, [0, 0, 0], [1.0, 1.0, 1.0 - blue_light_filter_strength])

    color_adjust_mode = key_engine.get_key("ColorFilterMode").get("value")
    if color_adjust_mode == "sync mobile":
        pass
        if mobile_filter is None: return frame
        if mobile_filter == "red_weak": return red_weak(frame)
        if mobile_filter == "green_weak": return green_weak(frame)
        if mobile_filter == "blue_weak": return blue_weak(frame)
        if mobile_filter == "all_weak": return all_weak(frame)
        return frame
    elif color_adjust_mode == "custom":
        pass
        red_boost = key_engine.get_key("ColorFilterRedBoost").get("value")
        green_boost = key_engine.get_key("ColorFilterGreenBoost").get("value")
        blue_boost = key_engine.get_key("ColorFilterBlueBoost").get("value")

        red_ratio = key_engine.get_key("ColorFilterRedRatio").get("value")
        green_ratio = key_engine.get_key("ColorFilterGreenRatio").get("value")
        blue_ratio = key_engine.get_key("ColorFilterBlueRatio").get("value")

        frame = adjust_frame(frame, [red_boost, green_boost, blue_boost], [red_ratio, green_ratio, blue_ratio])

        # frame[:, :, 2] = frame[:, :, 2] * red_ratio + red_boost
        # frame[:, :, 1] = frame[:, :, 1] * green_ratio + green_boost
        # frame[:, :, 0] = frame[:, :, 0] * blue_ratio + blue_boost
        # for x in range(320):
        #     pass
        #     for y in range(320):
        #         pass
        #         frame[y, x, 2] = frame[y, x, 2] * red_ratio + red_boost
        #         frame[y, x, 1] = frame[y, x, 1] * green_ratio + green_boost
        #         frame[y, x, 0] = frame[y, x, 0] * blue_ratio + blue_boost
    return frame
