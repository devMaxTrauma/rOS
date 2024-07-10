print("RKernel is booting up...")

print("defining pre def methods...")


def make_error(error_code: int, error_message: str):
    print("E" + str(error_code) + ": " + error_message)
    exit(error_code)


print("methods pre def defined.")

print("Loading Third Party imports...")
try:
    import cv2 as cv
except ImportError:
    make_error(1001, "cv2 not found.")
try:
    import time
except ImportError:
    make_error(1002, "time not found.")
try:
    import tensorflow as tf
except ImportError:
    make_error(1003, "tensorflow not found.")
try:
    import picamera2
except ImportError:
    print("Picamera2 not found.")
try:
    import threading
except ImportError:
    make_error(1005, "threading not found.")
try:
    import numpy as np
except ImportError:
    make_error(1006, "numpy not found.")
print("Third Party Imports loaded.")

print("Loading RKernel imports...")
try:
    import boot.RKey as key_engine
except ImportError:
    make_error(1101, "RKey not found.")
try:
    import boot.RSound as sound_engine
except ImportError:
    make_error(1102, "RSound not found.")
try:
    import boot.RFPS as fps_engine
except ImportError:
    make_error(1103, "RFPS not found.")
print("RKernel imports loaded.")

print("defining variables...")
splash_screen = cv.imread("boot/res/splash.png")
# init screen to required size
# if key_engine.get_key("ROSARDisplayEnabled").get("value"):
#     # screen size is ARDisplayWidth x ARDisplayHeight and make it dark
#     ar_width = key_engine.get_key("ARDisplayWidth").get("value")
#     ar_height = key_engine.get_key("ARDisplayHeight").get("value")
#     screen = [[0 for _ in range(ar_width)] for _ in range(ar_height)]
# else:
#     screen = [[0 for _ in range(320)] for _ in range(320)]
screen = splash_screen
raw_screen = splash_screen
tensor_thread = None
model = tf.lite.Interpreter(model_path="boot/res/model.tflite")
model.allocate_tensors()
model_input_details = model.get_input_details()
model_output_details = model.get_output_details()
print("variables defined.")

print("defining defs...")


def make_window():
    cv.namedWindow("ROS", cv.WINDOW_NORMAL)
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        ar_width = key_engine.get_key("ARDisplayWidth").get("value")
        ar_height = key_engine.get_key("ARDisplayHeight").get("value")
        cv.resizeWindow("ROS", ar_width, ar_height)
    else:
        cv.resizeWindow("ROS", 320, 320)


def get_camera():
    camera_device = key_engine.get_key("CameraDevice").get("value")
    if camera_device == "macbook pro":
        camera = cv.VideoCapture(0)
    elif camera_device == "iphone":
        camera = cv.VideoCapture(1)
    elif camera_device == "raspberry pi":
        camera = picamera2.Picamera2()
        camera.configure(camera.create_preview_configuration(main={"size": (320, 320)}))
        camera.start()
    else:
        print("warning! Invalid camera device. Using default device.")
        camera = cv.VideoCapture(0)
    return camera


def get_frame(camera):
    if key_engine.get_key("CameraDevice").get("value") == "raspberry pi":
        frame = camera.capture_array()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        if frame is None:
            print("raspberry pi camera read failed")
            return None
    else:
        capture_success, frame = camera.read()
        if not capture_success:
            print("camera read failed")
            return None

    # make frame 320x320
    if frame.shape[0] != 320 or frame.shape[1] != 320:
        # make new_frame but don't flect it
        target_width = 320
        target_height = 320
        aspect_ratio = float(target_height) / frame.shape[0]
        dsize = (int(frame.shape[1] * aspect_ratio), target_height)
        frame = cv.resize(frame, dsize)

        # cut the new_frame width to 320 center
        frame = frame[:,
                    frame.shape[1] // 2 - target_width // 2: frame.shape[1] // 2 + target_width // 2]
    return frame


def make_ar_frame(frame):
    if frame.shape[0] != 320 or frame.shape[1] != 320:
        target_width = 320
        target_height = 320
        aspect_ratio = float(target_height) / frame.shape[0]
        dsize = (int(frame.shape[1] * aspect_ratio), target_height)
        new_frame = cv.resize(frame, dsize)
        new_frame = new_frame[:,
                    new_frame.shape[1] // 2 - target_width // 2: new_frame.shape[1] // 2 + target_width // 2]
        frame = new_frame
        pass
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

        center_cross_bar_width = 0.01  # meter
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


def process_frame():
    while True:
        global raw_screen
        global model
        global model_input_details
        global model_output_details
        if model is None:
            return None
        # make sure that raw_screen is 320x320
        if raw_screen.shape[0] != 320 or raw_screen.shape[1] != 320:
            target_width = 320
            target_height = 320
            aspect_ratio = float(target_height) / raw_screen.shape[0]
            dsize = (int(raw_screen.shape[1] * aspect_ratio), target_height)
            raw_screen = cv.resize(raw_screen, dsize)
            raw_screen = raw_screen[:,
                         raw_screen.shape[1] // 2 - target_width // 2: raw_screen.shape[1] // 2 + target_width // 2]
        wip_screen = cv.cvtColor(raw_screen, cv.COLOR_BGR2RGB)
        wip_screen = np.expand_dims(wip_screen, axis=0)
        model.set_tensor(model_input_details[0]['index'], wip_screen)
        model.invoke()

        fps_engine.add_candidate_tensor_fps()


def render_tensor_and_etc(origin_frame):
    new_frame = origin_frame
    # render tensor todo late
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
    global main_screen_last_update_time
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        cv.imshow("ROS", make_ar_frame(screen))
    else:
        cv.imshow("ROS", screen)

    fps_engine.add_candidate_main_fps()


def shutdown():
    print("Shutting down...")
    # shutdown thread later todo
    tensor_thread.join()
    exit(0)

print("defs defined.")

print("preparing RKernel...")

if key_engine.get_key("ROSBootChimeEnabled").get("value"):
    sound_engine.play("boot/res/StartUp.mp3")

started_time = time.time()
splash_display_time = key_engine.get_key("ROSSplashScreenTime").get("value")
while time.time() - started_time < splash_display_time:
    tick_screen()
    if cv.waitKey(1) & 0xFF == 27:
        shutdown()

tensor_thread = threading.Thread(target=process_frame, args=()).start()
