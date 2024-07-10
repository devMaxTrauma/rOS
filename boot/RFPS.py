import time

tensor_last_update_time = time.time()
main_screen_last_update_time = time.time()
tensor_fps_history = []
main_screen_fps_history = []


def add_candidate_main_fps():
    global main_screen_last_update_time
    global main_screen_fps_history
    main_screen_fps_history.append(1 / (time.time() - main_screen_last_update_time))
    main_screen_last_update_time = time.time()
    if len(main_screen_fps_history) > 10:
        main_screen_fps_history.pop(0)
    return sum(main_screen_fps_history) / len(main_screen_fps_history)


def add_candidate_tensor_fps():
    global tensor_last_update_time
    global tensor_fps_history
    tensor_fps_history.append(1 / (time.time() - tensor_last_update_time))
    tensor_last_update_time = time.time()
    if len(tensor_fps_history) > 10:
        tensor_fps_history.pop(0)
    return sum(tensor_fps_history) / len(tensor_fps_history)


def get_main_screen_fps():
    if len(main_screen_fps_history) == 0:
        return -1
    return sum(main_screen_fps_history) / len(main_screen_fps_history)


def get_tensor_fps():
    if len(tensor_fps_history) == 0:
        return -1
    return sum(tensor_fps_history) / len(tensor_fps_history)
