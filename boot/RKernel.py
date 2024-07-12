print("RKernel is booting up...")

print("defining pre def methods...")


def make_error(error_code: str, error_message: str):
    print("E" + error_code + ": " + error_message)
    exit(error_code)


print("methods pre def defined.")

print("Loading Third Party imports...")
try:
    import cv2 as cv
except ImportError:
    make_error("1001", "cv2 not found.")
try:
    import time
except ImportError:
    make_error("1002", "time not found.")
try:
    import picamera2
except ImportError:
    print("Picamera2 not found.")
try:
    import threading
except ImportError:
    make_error("1005", "threading not found.")
try:
    import numpy as np
except ImportError:
    make_error("1006", "numpy not found.")
try:
    import sys
except ImportError:
    make_error("1007", "sys not found.")
try:
    import os
except ImportError:
    make_error("1008", "os not found.")
print("Third Party Imports loaded.")

print("Loading RKernel imports...")
try:
    import boot.RKey as key_engine
except ImportError:
    make_error("1101", "RKey not found.")
try:
    import boot.RSound as sound_engine
except ImportError:
    make_error("1102", "RSound not found.")
try:
    import boot.RFPS as fps_engine
except ImportError:
    make_error("1103", "RFPS not found.")
try:
    import boot.RTensor as tensor_engine
except ImportError:
    make_error("1104", "RTensor not found.")
except Exception as e:
    make_error("1104-1", str(e))
try:
    import boot.RLabel as label_engine
except ImportError:
    make_error("1105", "RLabel not found.")
try:
    import boot.RColor as color_engine
except ImportError:
    make_error("1106", "RColor not found.")
try:
    import boot.RBluetooth as bluetooth_engine
except ImportError as e:
    print("RBluetooth not found.")
print("RKernel imports loaded.")

print("defining variables...")
splash_screen = cv.imread("boot/res/apple_logo.png")
screen = splash_screen
raw_screen = splash_screen
camera = None
find_my_keep_sounding_channel = None
find_my_sounding_one_channel = None
print("variables defined.")

print("defining defs...")


def get_320_320_frame(raw_frame):
    if raw_frame is None:
        raw_frame = cv.imread("boot/res/black_screen.jpg")
    # make sure the frame is 320x320 and save it to raw_frame
    if raw_frame.shape[0] != 320 or raw_frame.shape[1] != 320:
        # make new_frame but don't flect it
        target_width = 320
        target_height = 320
        aspect_ratio = float(target_height) / raw_frame.shape[0]
        dsize = (int(raw_frame.shape[1] * aspect_ratio), target_height)
        raw_frame = cv.resize(raw_frame, dsize)

        # cut the new_frame width to 320 center
        raw_frame = raw_frame[:,
                    raw_frame.shape[1] // 2 - target_width // 2: raw_frame.shape[1] // 2 + target_width // 2]
    return raw_frame


def make_window():
    cv.namedWindow("ROS", cv.WINDOW_NORMAL)
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        ar_width = key_engine.get_key("ARDisplayWidth").get("value")
        ar_height = key_engine.get_key("ARDisplayHeight").get("value")
        cv.resizeWindow("ROS", ar_width, ar_height)
    else:
        cv.resizeWindow("ROS", 320, 320)


def get_camera():
    if "picamera2" in sys.modules:
        camera = picamera2.Picamera2()
        camera.configure(camera.create_preview_configuration(main={"size": (320, 320)}))
        camera.start()
    else:
        camera = cv.VideoCapture(0)
    return camera


def get_frame():
    global camera
    if "picamera2" in sys.modules:
        frame = camera.capture_array()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    else:
        frame = camera.read()[1]

    if frame is None:
        print("camera read failed")
        return None

    # make frame 320x320
    return get_320_320_frame(frame)


def calculate_distance(class_index:int, box_width_pixel):
    if "picamera2" in sys.modules:
        distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantRaspberryPi").get("value")
    else:
        distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantMacBookPro").get("value")

    if label_engine.get_label(class_index+1) is None:
        object_average_width = -1.0
    else:
        object_average_width = label_engine.get_label(class_index+1).get("average_width")

    if object_average_width == -1.0:
        return str("N/A")

    distance_in_meter = object_average_width/(box_width_pixel/distance_calculate_constant)
    unit = key_engine.get_key("DistanceUnit").get("value")
    if unit == "SI" and distance_in_meter < 1:
        return str(round(distance_in_meter * 100, 2)) + " cm"
    elif unit == "SI" and distance_in_meter <= 1000:
        return str(round(distance_in_meter, 2)) + " m"
    elif unit == "SI" and distance_in_meter > 1000:
        return str(round(distance_in_meter / 1000, 2)) + " km"
    elif unit == "US" and distance_in_meter < 0.3048:
        return str(round(distance_in_meter * 39.3701, 2)) + " in"
    elif unit == "US" and distance_in_meter <= 0.9144:
        return str(round(distance_in_meter * 3.28084, 2)) + " ft"
    elif unit == "US" and distance_in_meter <= 1609.34:
        return str(round(distance_in_meter * 1.09361, 2)) + " yd"
    elif unit == "US" and distance_in_meter > 1609.34:
        return str(round(distance_in_meter / 1609.34, 2)) + " mi"
    else:
        return str("ERR")




def make_ar_frame(frame):
    # make sure that input frame is 320x320
    frame = get_320_320_frame(frame)
    # frame input resolution: 320 320
    ar_width = key_engine.get_key("ARDisplayWidth").get("value")
    ar_height = key_engine.get_key("ARDisplayHeight").get("value")
    ar_ppi = key_engine.get_key("ARDisplayPPI").get("value")
    user_eye_distance = key_engine.get_key("AREyeDistance").get("value")  # meter

    ar_screen = np.zeros((ar_height, ar_width, 3), np.uint8)
    ar_screen = cv.cvtColor(ar_screen, cv.COLOR_BGR2RGB)

    eye_distance_to_inch = user_eye_distance * 39.3701
    eye_distance_to_pixel = int(eye_distance_to_inch * ar_ppi)

    left_eye_center_x = (ar_width // 2) - (eye_distance_to_pixel // 2)
    right_eye_center_x = (ar_width // 2) + (eye_distance_to_pixel // 2)
    eye_center_y = ar_height // 2

    left_eye_start_x = left_eye_center_x - (320 // 2)
    right_eye_start_x = right_eye_center_x - (320 // 2)
    eye_start_y = eye_center_y - (320 // 2)

    preferred_eye = key_engine.get_key("ARPreferredEye").get("value")

    if key_engine.get_key("ARMode").get("value") == "both eye":
        # new version
        left_eye_screen = frame
        right_eye_screen = frame

        center_cross_bar_width = 0.005  # meter
        center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)

        left_eye_max_x = (ar_width - center_cross_bar_width_pixel) // 2
        right_eye_min_x = (ar_width + center_cross_bar_width_pixel) // 2

        left_eye_screen_width = left_eye_max_x - left_eye_start_x
        right_eye_screen_width = right_eye_start_x + 320 - right_eye_min_x

        left_eye_screen = left_eye_screen[:, 0:left_eye_screen_width]
        right_eye_screen = right_eye_screen[:, 320 - right_eye_screen_width:]

        ar_screen[eye_start_y:eye_start_y + 320,
        left_eye_start_x:left_eye_start_x + left_eye_screen_width] = left_eye_screen
        ar_screen[eye_start_y:eye_start_y + 320,
        right_eye_start_x + 320 - right_eye_screen_width:right_eye_start_x + 320] = right_eye_screen

    elif key_engine.get_key("ARMode").get("value") == "one eye" and preferred_eye == "left":
        # ar_screen[eye_start_y:eye_start_y + 320, left_eye_start_x:left_eye_start_x + 320] = frame
        left_eye_screen = frame

        center_cross_bar_width = 0.01  # meter
        center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)

        left_eye_max_x = (ar_width - center_cross_bar_width_pixel) // 2
        left_eye_screen_width = left_eye_max_x - left_eye_start_x
        left_eye_screen = left_eye_screen[:, 0:left_eye_screen_width]

        ar_screen[eye_start_y:eye_start_y + 320,
        left_eye_start_x:left_eye_start_x + left_eye_screen_width] = left_eye_screen
        pass

    elif key_engine.get_key("ARMode").get("value") == "one eye" and preferred_eye == "right":  # copy right eye
        # ar_screen[eye_start_y:eye_start_y + 320, right_eye_start_x:right_eye_start_x + 320] = frame
        right_eye_screen = frame

        center_cross_bar_width = 0.01  # meter
        center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)

        right_eye_min_x = (ar_width + center_cross_bar_width_pixel) // 2
        right_eye_screen_width = right_eye_start_x + 320 - right_eye_min_x
        right_eye_screen = right_eye_screen[:, 320 - right_eye_screen_width:]

        ar_screen[eye_start_y:eye_start_y + 320,
        right_eye_start_x + 320 - right_eye_screen_width:right_eye_start_x + 320] = right_eye_screen
        pass

    return ar_screen


def render_tensor(screen, boxes, classes, scores, distance):
    if scores < 0.5:
        return screen
    box = boxes * [320, 320, 320, 320]
    class_name = label_engine.get_label(int(classes + 1)).get("value")
    class_color = color_engine.get_color(class_name)
    inverted_color = (255 - class_color[0], 255 - class_color[1], 255 - class_color[2])
    text_x, text_y = 0, 0  # for text position
    if key_engine.get_key("ROSMindDisplayWay").get("value") == "filled box":
        # outer line
        cv.rectangle(screen, (int(box[1]), int(box[0]), int(box[3]), int(box[2])), inverted_color, 2)
        # inner box
        cv.rectangle(screen, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), class_color, -1)
        # put text center of the box
        text_size = cv.getTextSize(class_name, cv.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        text_x = int((box[1] + box[3]) / 2 - text_size[0] / 2)
        text_y = int((box[0] + box[2]) / 2 + text_size[1] / 2)
        cv.putText(screen, class_name, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   inverted_color, 2)
    elif key_engine.get_key("ROSMindDisplayWay").get("value") == "outlined box":
        cv.rectangle(screen, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), class_color, 2)
        text_x = int(box[1])
        text_y = int(box[0])
        cv.putText(screen, class_name, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   class_color, 2)

    if key_engine.get_key("DistanceDisplayEnabled").get("value"):
        cv.putText(screen, str(distance), (text_x, text_y + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   inverted_color, 1, cv.LINE_AA)

    return screen


def render_tensors(tensor_output):
    global raw_screen
    boxes, classes, scores, distance = tensor_output
    in_print_screen = raw_screen
    for i in range(len(scores)):
        in_print_screen = render_tensor(in_print_screen, boxes[i], classes[i], scores[i], distance[i])
    return in_print_screen


def render_tensor_and_etc():
    global raw_screen
    new_frame = raw_screen
    # render tensor
    tensor_output = tensor_engine.tensor_output
    if tensor_output is not None:
        new_frame = render_tensors(tensor_output)
    # render etc
    # render fps
    if key_engine.get_key("ROSDisplayFPSEnable").get("value"):
        main_screen_fps = round(fps_engine.get_main_screen_fps(), 2)
        tensor_fps = round(fps_engine.get_tensor_fps(), 2)
        cv.putText(new_frame, "MS FPS: " + str(main_screen_fps), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(new_frame, " T FPS: " + str(tensor_fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                   1, cv.LINE_AA)
    global screen
    screen = new_frame
    return new_frame


def tick_screen():
    make_window()
    global screen
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        cv.imshow("ROS", make_ar_frame(screen))
    else:
        cv.imshow("ROS", screen)

    fps_engine.add_candidate_main_fps()


def set_tensor_input():
    global raw_screen
    raw_screen = get_320_320_frame(raw_screen)
    raw_data = cv.cvtColor(raw_screen, cv.COLOR_BGR2RGB)
    raw_data = np.expand_dims(raw_data, axis=0)
    tensor_engine.raw_data = raw_data


def shutdown():
    print("Shutting down...")
    global camera
    # shutdown thread later
    tensor_engine.stop_process_frame()
    label_engine.erase_memory()
    color_engine.erase_memory()
    if "boot.RBluetooth" in sys.modules:
        bluetooth_engine.close()
    key_engine.save_keys()
    cv.destroyAllWindows()
    if "picamera2" in sys.modules:
        camera.stop()
    else:
        camera.release()
    current_threads = threading.enumerate()
    for thread in current_threads:
        if thread.name == "MainThread": continue
        print("Thread " + thread.name + " is in running.")
    if len(current_threads) > 1:
        print("There are still threads running.")
        print("Force shutdown.")
        os._exit(0)
    print("Shutdown complete.")
    exit(0)


def bluetooth_connected_callback():
    sound_engine.play("boot/res/alert.mp3")
    print("Bluetooth connected.")


def bluetooth_signal_callback(data):
    global find_my_sounding_one_channel
    global find_my_keep_sounding_channel
    if data == b"a":
        sound_engine.stop(find_my_sounding_one_channel)
        find_my_sounding_one_channel = sound_engine.play("boot/res/FindMy.mp3")
    elif data == b"b":
        find_my_keep_sounding_channel = sound_engine.play("boot/res/FindMy.mp3", -1)
        pass
    elif data == b"c":
        sound_engine.stop(find_my_keep_sounding_channel)
        pass


print("defs defined.")

print("preparing RKernel...")
tensor_engine.fps_engine = fps_engine
tensor_engine.calculate_distance_function = calculate_distance
if "boot.RBluetooth" in sys.modules:
    print("callback set.")
    bluetooth_engine.connected_callback = bluetooth_connected_callback
    bluetooth_engine.recv_callback = bluetooth_signal_callback
camera = get_camera()

# set_tensor_input()
if key_engine.get_key("ROSBootChimeEnabled").get("value"):
    sound_engine.play("boot/res/StartUp.mp3")

started_time = time.time()
splash_display_time = key_engine.get_key("ROSSplashScreenTime").get("value")
while time.time() - started_time < splash_display_time:
    tick_screen()
    if cv.waitKey(1) & 0xFF == 27:
        shutdown()
