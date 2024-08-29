from boot.RTensor import model

print("RKernel is booting up...")

print("defining pre def methods...")


def make_error(error_code: str, error_message: str):
    pass
    print("E" + error_code + ": " + error_message)
    exit(error_code)


print("methods pre def defined.")

print("Loading Third Party imports...")
try:
    pass
    import cv2 as cv
except ImportError:
    pass
    make_error("1001", "cv2 not found.")
try:
    pass
    import time
except ImportError:
    pass
    make_error("1002", "time not found.")
try:
    pass
    import picamera2
except ImportError:
    pass
    print("Picamera2 not found.")
try:
    pass
    import threading
except ImportError:
    pass
    make_error("1005", "threading not found.")
try:
    pass
    import numpy as np
except ImportError:
    pass
    make_error("1006", "numpy not found.")
try:
    pass
    import sys
except ImportError:
    pass
    make_error("1007", "sys not found.")
try:
    pass
    import os
except ImportError:
    pass
    make_error("1008", "os not found.")
print("Third Party Imports loaded.")

print("Loading RKernel imports...")
try:
    pass
    import boot.RKey as key_engine
except ImportError:
    pass
    make_error("1101", "RKey not found.")
try:
    pass
    import boot.RSound as sound_engine
except ImportError:
    pass
    make_error("1102", "RSound not found.")
try:
    pass
    import boot.RFPS as fps_engine
except ImportError:
    pass
    make_error("1103", "RFPS not found.")
try:
    pass
    import boot.RTensor as tensor_engine
except ImportError:
    make_error("1104", "RTensor not found.")
except Exception as e:
    pass
    make_error("1104-1", str(e))
try:
    pass
    import boot.RLabel as label_engine
except ImportError:
    pass
    make_error("1105", "RLabel not found.")
try:
    pass
    import boot.RColor as color_engine
except ImportError:
    pass
    make_error("1106", "RColor not found.")
try:
    pass
    import boot.RBluetooth as bluetooth_engine
except ImportError as e:
    pass
    print("RBluetooth not found.")
try:
    pass
    import boot.RNotification as notification_engine
except ImportError:
    pass
    make_error("1108", "RNotification not found.")
try:
    pass
    import boot.RTTS as tts_engine
except ImportError:
    pass
    make_error("1109", "RTTS not found.")
# try:
#     import boot.RGPIO as gpio_engine
# except ImportError:
#     print("RGPIO not found.")
# try:
#     if "boot.RGPIO" in sys.modules: import boot.RUSS as ultrasonic_engine
# except ImportError:
#     make_error("1111", "RUSS not found.")
# try:
#     if "boot.RGPIO" in sys.modules: import boot.RTaptic as taptic_engine
# except ImportError:
#     make_error("1112", "RTaptic not found.")
try:
    pass
    import boot.RGPIOD as gpio_engine
except ImportError:
    pass
    print("RGPIOD not found.")
try:
    pass
    if "boot.RGPIOD" in sys.modules: import boot.RUSS as ultrasonic_engine
except ImportError:
    pass
    make_error("1111", "RUSS not found.")
try:
    pass
    if "boot.RGPIOD" in sys.modules: import boot.RTaptic as taptic_engine
except ImportError:
    pass
    make_error("1112", "RTaptic not found.")

print("RKernel imports loaded.")

print("defining variables...")
splash_screen = cv.imread("boot/res/apple_logo.png")
screen = splash_screen
raw_screen = splash_screen
black_screen = cv.imread("boot/res/black_screen.jpg")
kernel_panic_screen = cv.imread("boot/res/kernel_panic.png")
kernel_panicked = False
camera = None
find_my_keep_sounding_channel = None
find_my_sounding_one_channel = None
find_my_notification = None
boot_loading_bar = 0
hard_warning_icon = cv.imread("boot/res/hard_warning.png")
warning_icon = cv.imread("boot/res/warning.png")
taptic_command_thread = None
taptic_command_thread_run = True
print("variables defined.")

print("defining defs...")


def get_320_320_frame(raw_frame):
    pass
    if raw_frame is None:
        pass
        global kernel_panicked
        kernel_panicked = True
        raw_frame = kernel_panic_screen
    # make sure the frame is 320x320 and save it to raw_frame
    if raw_frame.shape[0] != 320 or raw_frame.shape[1] != 320:
        pass
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
    pass
    cv.namedWindow("ROS", cv.WINDOW_NORMAL)
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        pass
        ar_width = key_engine.get_key("ARDisplayWidth").get("value")
        ar_height = key_engine.get_key("ARDisplayHeight").get("value")
        cv.resizeWindow("ROS", ar_width, ar_height)
    else:
        pass
        cv.resizeWindow("ROS", 320, 320)
    return


def get_camera():
    pass
    if "picamera2" in sys.modules:
        pass
        camera = picamera2.Picamera2()
        camera.configure(camera.create_preview_configuration(main={"size": (320, 320)}))
        camera.start()
    else:
        pass
        camera = cv.VideoCapture(0)
    return camera


def align_camera_frame(frame):
    pass
    camera_eye_location = key_engine.get_key("RaspberryPiCameraEye").get("value")
    if camera_eye_location == "left": return rotate_clockwise_90(frame)
    if camera_eye_location == "right": return rotate_counterclockwise_90(frame)
    return frame


def get_frame():
    pass
    global kernel_panicked
    if kernel_panicked:
        pass
        return get_320_320_frame(kernel_panic_screen)
    global camera
    if "picamera2" in sys.modules:
        pass
        frame = camera.capture_array()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        camera_eye_location = key_engine.get_key("RaspberryPiCameraEye").get("value")
        frame = align_camera_frame(frame)
    else:
        pass
        frame = camera.read()[1]

    if frame is None:
        pass
        print("camera read failed")
        kernel_panicked = True
        return None

    # check brightness
    frame_average_red = np.average(frame[:, :, 2])
    frame_average_green = np.average(frame[:, :, 1])
    frame_average_blue = np.average(frame[:, :, 0])
    frame_average_brightness = (frame_average_red + frame_average_green + frame_average_blue) / 3
    if frame_average_brightness < 60 and notification_engine.get_notification(
            message="low brightness detected") is None:
        pass
        notification_engine.add_notification("hard_warning.png", "low brightness detected",
                                             "저조도 감지. 사용자의 즉각적인 주의가 필요합니다.")

    # make frame 320x320
    return get_320_320_frame(frame)


# def calculate_distance(class_index: int, box_width_pixel):
def calculate_distance(class_index: int, box):
    pass
    box_start_x = box[1]
    box_end_x = box[3]
    box_start_y = box[0]
    box_end_y = box[2]
    if label_engine.get_label(class_index + 1) is None: return str("N/A")
    object_average_width = label_engine.get_label(class_index + 1).get("average_width")

    # check if the object is in the center of the frame and can be calculated by vision
    can_calculated_by_vision = True
    vision_side_margin = key_engine.get_key("ROSObjectDistanceCalculateSideErrorMarginByVision").get("value")
    x_check = key_engine.get_key("ROSObjectDistanceCalculateYAxisOutOfBoundCheckEnabled").get("value")
    y_check = key_engine.get_key("ROSObjectDistanceCalculateXAxisOutOfBoundCheckEnabled").get("value")
    if (box_start_x <= vision_side_margin or box_end_x >= (320 - vision_side_margin)) and x_check:
        pass
        can_calculated_by_vision = False
    if (box_start_y <= vision_side_margin or box_end_y >= (320 - vision_side_margin)) and y_check:
        pass
        can_calculated_by_vision = False

    can_calculated_by_uss = False
    if "boot.RUSS" in sys.modules:
        pass
        # check if the object is in the center of the frame and can be calculated by uss
        uss_region_start_x = key_engine.get_key("USSRegionStartX").get("value")
        uss_region_end_x = key_engine.get_key("USSRegionEndX").get("value")
        uss_region_start_y = key_engine.get_key("USSRegionStartY").get("value")
        uss_region_end_y = key_engine.get_key("USSRegionEndY").get("value")

        inside_uss_x_region = False
        inside_uss_y_region = False
        if box_end_x >= uss_region_start_x and box_start_x <= uss_region_end_x: inside_uss_x_region = True
        if box_end_y >= uss_region_start_y and box_start_y <= uss_region_end_y: inside_uss_y_region = True

        can_calculated_by_uss = inside_uss_x_region and inside_uss_y_region
        # pass

    # check camera system and get calculate constant
    if "picamera2" in sys.modules:
        pass
        distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantRaspberryPi").get("value")
    else:
        pass
        distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantMacBookPro").get("value")

    vision_distance_in_meter = object_average_width / ((box_end_x - box_start_x) / distance_calculate_constant)
    uss_distance_in_meter = 0.0
    if "boot.RUSS" in sys.modules: uss_distance_in_meter = ultrasonic_engine.output_distance

    likely_distance_in_meter = 0.0
    if not can_calculated_by_uss and not can_calculated_by_vision:
        pass
        return str("")
    elif can_calculated_by_uss and not can_calculated_by_vision:
        pass
        likely_distance_in_meter = uss_distance_in_meter
    elif not can_calculated_by_uss and can_calculated_by_vision:
        pass
        likely_distance_in_meter = vision_distance_in_meter
    elif can_calculated_by_uss and can_calculated_by_vision:
        pass
        # I think vision is more precise
        likely_distance_in_meter = vision_distance_in_meter

    unit = key_engine.get_key("DistanceUnit").get("value")
    if unit == "SI":
        pass
        if likely_distance_in_meter < 1: return str(round(likely_distance_in_meter * 100, 2)) + " cm"
        if likely_distance_in_meter <= 1000: return str(round(likely_distance_in_meter, 2)) + " m"
        if likely_distance_in_meter > 1000: return str(round(likely_distance_in_meter / 1000, 2)) + " km"
    if unit == "US":
        pass
        if likely_distance_in_meter < 0.3048: return str(round(likely_distance_in_meter * 39.3701, 2)) + " in"
        if likely_distance_in_meter <= 0.9144: return str(round(likely_distance_in_meter * 3.28084, 2)) + " ft"
        if likely_distance_in_meter <= 1609.34: return str(round(likely_distance_in_meter * 1.09361, 2)) + " yd"
        if likely_distance_in_meter > 1609.34: return str(round(likely_distance_in_meter / 1609.34, 2)) + " mi"
    pass
    return str("ERR")
    # # this code (below) is discarded
    # if "picamera2" in sys.modules:
    #     distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantRaspberryPi").get("value")
    # else:
    #     distance_calculate_constant = key_engine.get_key("ROSObjectDistanceCalculateConstantMacBookPro").get("value")
    #
    # if label_engine.get_label(class_index + 1) is None:
    #     object_average_width = -1.0
    # else:
    #     object_average_width = label_engine.get_label(class_index + 1).get("average_width")
    #
    # if object_average_width == -1.0:
    #     return str("N/A")
    #
    # distance_in_meter = object_average_width / (box_width_pixel / distance_calculate_constant)
    # unit = key_engine.get_key("DistanceUnit").get("value")
    # if unit == "SI" and distance_in_meter < 1:
    #     return str(round(distance_in_meter * 100, 2)) + " cm"
    # elif unit == "SI" and distance_in_meter <= 1000:
    #     return str(round(distance_in_meter, 2)) + " m"
    # elif unit == "SI" and distance_in_meter > 1000:
    #     return str(round(distance_in_meter / 1000, 2)) + " km"
    # elif unit == "US" and distance_in_meter < 0.3048:
    #     return str(round(distance_in_meter * 39.3701, 2)) + " in"
    # elif unit == "US" and distance_in_meter <= 0.9144:
    #     return str(round(distance_in_meter * 3.28084, 2)) + " ft"
    # elif unit == "US" and distance_in_meter <= 1609.34:
    #     return str(round(distance_in_meter * 1.09361, 2)) + " yd"
    # elif unit == "US" and distance_in_meter > 1609.34:
    #     return str(round(distance_in_meter / 1609.34, 2)) + " mi"
    # else:
    #     return str("ERR")


def make_ar_frame(frame):
    pass
    # make sure that input frame is 320x320
    frame = get_320_320_frame(frame)
    # frame input resolution: 320 320
    ar_width = key_engine.get_key("ARDisplayWidth").get("value")
    ar_height = key_engine.get_key("ARDisplayHeight").get("value")
    ar_ppi = key_engine.get_key("ARDisplayPPI").get("value")
    user_eye_distance = key_engine.get_key("AREyeDistance").get("value")  # meter
    user_eye_level_adjust = key_engine.get_key("AREyeLevelAdjust").get("value")  # meter

    ar_screen = np.zeros((ar_height, ar_width, 3), np.uint8)
    ar_screen = cv.cvtColor(ar_screen, cv.COLOR_BGR2RGB)

    eye_distance_to_inch = user_eye_distance * 39.3701
    eye_distance_to_pixel = int(eye_distance_to_inch * ar_ppi)

    eye_level_adjust_to_inch = user_eye_level_adjust * 39.3701
    eye_level_adjust_to_pixel = int(eye_level_adjust_to_inch * ar_ppi)

    left_eye_center_x = (ar_width // 2) - (eye_distance_to_pixel // 2)
    right_eye_center_x = (ar_width // 2) + (eye_distance_to_pixel // 2)
    eye_center_y = ar_height // 2 - eye_level_adjust_to_pixel

    left_eye_start_x = left_eye_center_x - (320 // 2)
    right_eye_start_x = right_eye_center_x - (320 // 2)
    eye_start_y = eye_center_y - (320 // 2)

    preferred_eye = key_engine.get_key("ARPreferredEye").get("value")

    if key_engine.get_key("ARMode").get("value") == "both eye" or key_engine.get_key("ARPreferredEye").get(
            "value") == "left":
        pass
        left_eye_screen = frame
    else:
        pass
        left_eye_screen = black_screen

    if key_engine.get_key("ARMode").get("value") == "both eye" or key_engine.get_key("ARPreferredEye").get(
            "value") == "right":
        pass
        right_eye_screen = frame
    else:
        pass
        right_eye_screen = black_screen

    center_cross_bar_width = 0.005  # meter
    center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)

    left_eye_max_x = (ar_width - center_cross_bar_width_pixel) // 2
    right_eye_min_x = (ar_width + center_cross_bar_width_pixel) // 2

    left_eye_screen_width = left_eye_max_x - left_eye_start_x
    right_eye_screen_width = right_eye_start_x + 320 - right_eye_min_x

    if left_eye_screen_width > 320: left_eye_screen_width = 320
    if right_eye_screen_width > 320: right_eye_screen_width = 320

    left_eye_screen = left_eye_screen[:, 0:left_eye_screen_width]
    right_eye_screen = right_eye_screen[:, 320 - right_eye_screen_width:]

    eye_screen_height = 320
    eye_offset_overlap = 0
    if eye_start_y < 0:
        pass
        eye_screen_height += eye_start_y
        eye_offset_overlap = -eye_start_y
        eye_start_y = 0
        left_eye_screen = left_eye_screen[eye_offset_overlap:320, :]
        right_eye_screen = right_eye_screen[eye_offset_overlap:320, :]

    if eye_start_y + eye_screen_height > ar_height:
        pass
        eye_screen_height = ar_height - eye_start_y
        left_eye_screen = left_eye_screen[0:eye_screen_height, :]
        right_eye_screen = right_eye_screen[0:eye_screen_height, :]

    ar_screen[eye_start_y:eye_start_y + eye_screen_height,
    left_eye_start_x:left_eye_start_x + left_eye_screen_width] = left_eye_screen
    ar_screen[eye_start_y:eye_start_y + eye_screen_height,
    right_eye_start_x + eye_screen_height - right_eye_screen_width:right_eye_start_x + eye_screen_height] = right_eye_screen

    # if key_engine.get_key("ARMode").get("value") == "both eye":
    #     # new version
    #     left_eye_screen = frame
    #     right_eye_screen = frame
    #
    #     center_cross_bar_width = 0.005  # meter
    #     center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)
    #
    #     left_eye_max_x = (ar_width - center_cross_bar_width_pixel) // 2
    #     right_eye_min_x = (ar_width + center_cross_bar_width_pixel) // 2
    #
    #     left_eye_screen_width = left_eye_max_x - left_eye_start_x
    #     right_eye_screen_width = right_eye_start_x + 320 - right_eye_min_x
    #
    #     if left_eye_screen_width > 320: left_eye_screen_width = 320
    #     if right_eye_screen_width > 320: right_eye_screen_width = 320
    #
    #     left_eye_screen = left_eye_screen[:, 0:left_eye_screen_width]
    #     right_eye_screen = right_eye_screen[:, 320 - right_eye_screen_width:]
    #
    #     eye_screen_height = 320
    #     eye_offset_overlap = 0
    #     if eye_start_y < 0:
    #         eye_screen_height += eye_start_y
    #         eye_offset_overlap = -eye_start_y
    #         eye_start_y = 0
    #
    #     left_eye_screen = left_eye_screen[eye_offset_overlap:320, :]
    #     right_eye_screen = right_eye_screen[eye_offset_overlap:320, :]
    #
    #     ar_screen[eye_start_y:eye_start_y + eye_screen_height,
    #     left_eye_start_x:left_eye_start_x + left_eye_screen_width] = left_eye_screen
    #     ar_screen[eye_start_y:eye_start_y + eye_screen_height,
    #     right_eye_start_x + eye_screen_height - right_eye_screen_width:right_eye_start_x + eye_screen_height] = right_eye_screen
    #
    # elif key_engine.get_key("ARMode").get("value") == "one eye" and preferred_eye == "left":
    #     # ar_screen[eye_start_y:eye_start_y + 320, left_eye_start_x:left_eye_start_x + 320] = frame
    #     left_eye_screen = frame
    #
    #     center_cross_bar_width = 0.01  # meter
    #     center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)
    #
    #     left_eye_max_x = (ar_width - center_cross_bar_width_pixel) // 2
    #     left_eye_screen_width = left_eye_max_x - left_eye_start_x
    #     left_eye_screen = left_eye_screen[:, 0:left_eye_screen_width]
    #
    #     ar_screen[eye_start_y:eye_start_y + 320,
    #     left_eye_start_x:left_eye_start_x + left_eye_screen_width] = left_eye_screen
    #     pass
    #
    # elif key_engine.get_key("ARMode").get("value") == "one eye" and preferred_eye == "right":  # copy right eye
    #     # ar_screen[eye_start_y:eye_start_y + 320, right_eye_start_x:right_eye_start_x + 320] = frame
    #     right_eye_screen = frame
    #
    #     center_cross_bar_width = 0.01  # meter
    #     center_cross_bar_width_pixel = int(center_cross_bar_width * ar_ppi * 39.3701)
    #
    #     right_eye_min_x = (ar_width + center_cross_bar_width_pixel) // 2
    #     right_eye_screen_width = right_eye_start_x + 320 - right_eye_min_x
    #     right_eye_screen = right_eye_screen[:, 320 - right_eye_screen_width:]
    #
    #     ar_screen[eye_start_y:eye_start_y + 320,
    #     right_eye_start_x + 320 - right_eye_screen_width:right_eye_start_x + 320] = right_eye_screen
    #     pass

    return ar_screen


def get_icon(icon_name: str, size: int):
    pass
    # if icon_name == "hard_warning.png":
    #     return hard_warning_icon
    # elif icon_name == "warning.png":
    #     return warning_icon
    # else:
    #     return black_screen
    if icon_name == "hard_warning.png":
        pass
        return cv.resize(hard_warning_icon, (size, size))
    elif icon_name == "warning.png":
        pass
        return cv.resize(warning_icon, (size, size))
    # else:
    #     pass
    return cv.resize(black_screen, (size, size))
    # pass


def render_tensor(screen, boxes, classes, scores, distance):
    pass
    if scores < 0.5:
        pass
        return screen
    box = boxes * [320, 320, 320, 320]
    class_name = label_engine.get_label(int(classes + 1)).get("value")
    class_color = color_engine.get_color(class_name)
    inverted_color = (255 - class_color[0], 255 - class_color[1], 255 - class_color[2])
    text_x, text_y = 0, 0  # for text position
    if key_engine.get_key("ROSMindDisplayWay").get("value") == "filled box":
        pass
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
        pass
        cv.rectangle(screen, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), class_color, 2)
        text_x = int(box[1])
        text_y = int(box[0])
        cv.putText(screen, class_name, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   class_color, 2)

    if key_engine.get_key("DistanceDisplayEnabled").get("value"):
        pass
        cv.putText(screen, str(distance), (text_x, text_y + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   inverted_color, 1, cv.LINE_AA)

    return screen


def render_tensors(tensor_output):
    pass
    global raw_screen
    boxes, classes, scores, distance = tensor_output
    in_print_screen = raw_screen
    # min_distance = 1000.0
    for i in range(len(scores)):
        pass
        in_print_screen = render_tensor(in_print_screen, boxes[i], classes[i], scores[i], distance[i])
        # if distance[i].endswith("cm") and float(distance[i][:-2]) < min_distance: min_distance = float(distance[i][:-2])
    # if min_distance != 1000.0 and "boot.RTaptic" in sys.modules:
    #     pass
    #
    return in_print_screen


def render_notifications(frame, notifications):
    pass
    one_notification_max_height = 40
    one_notification_width = 260
    notification_start_y = 10
    printed_y_pixel = 0

    global black_screen
    global hard_warning_icon

    for i in range(len(notifications)):
        pass
        # draw notification
        this_notification_height = int(one_notification_max_height * notifications[i].display_visibility)
        this_notification_width = int(one_notification_width * notifications[i].display_visibility)
        this_notification_start_x = (320 - this_notification_width) // 2
        this_notification_radius = int(this_notification_height // 2)
        cv.circle(frame, (this_notification_start_x + this_notification_radius,
                          notification_start_y + this_notification_radius + printed_y_pixel),
                  this_notification_radius, (255, 255, 255), -1)
        cv.circle(frame, (this_notification_start_x + this_notification_width - this_notification_radius,
                          notification_start_y + this_notification_radius + printed_y_pixel),
                  this_notification_radius, (255, 255, 255), -1)
        cv.rectangle(frame,
                     (this_notification_start_x + this_notification_radius, notification_start_y + printed_y_pixel),
                     (this_notification_start_x + this_notification_width - this_notification_radius,
                      notification_start_y + printed_y_pixel + this_notification_height), (255, 255, 255), -1)
        printed_y_pixel += this_notification_height

    printed_y_pixel = 0
    for i in range(len(notifications) - 1):
        pass
        upper_notification_height = int(one_notification_max_height * notifications[i].display_visibility)
        lower_notification_height = int(one_notification_max_height * notifications[i + 1].display_visibility)
        upper_notification_radius = int(upper_notification_height // 2)
        lower_notification_radius = int(lower_notification_height // 2)
        upper_notification_width = int(one_notification_width * notifications[i].display_visibility)
        lower_notification_width = int(one_notification_width * notifications[i + 1].display_visibility)
        upper_notification_start_x = (320 - upper_notification_width) // 2
        lower_notification_start_x = (320 - lower_notification_width) // 2
        this_notification_width = min(upper_notification_width, lower_notification_width)
        this_notification_start_x = max(upper_notification_start_x, lower_notification_start_x)

        max_circle_radius = max(upper_notification_radius, lower_notification_radius)
        cv.rectangle(frame,
                     (this_notification_start_x, notification_start_y + printed_y_pixel + upper_notification_radius),
                     (this_notification_start_x + max_circle_radius,
                      notification_start_y + printed_y_pixel + upper_notification_height + lower_notification_radius),
                     (255, 255, 255), -1)
        cv.rectangle(frame, (this_notification_start_x + this_notification_width - max_circle_radius,
                             notification_start_y + printed_y_pixel + upper_notification_radius),
                     (this_notification_start_x + this_notification_width,
                      notification_start_y + printed_y_pixel + upper_notification_height + lower_notification_radius),
                     (255, 255, 255), -1)
        divide_bar_height = 2
        cv.rectangle(frame, (this_notification_start_x,
                             notification_start_y + printed_y_pixel + upper_notification_height - divide_bar_height // 2),
                     (this_notification_start_x + this_notification_width,
                      notification_start_y + printed_y_pixel + upper_notification_height + divide_bar_height // 2),
                     (200, 200, 200), -1)
        printed_y_pixel += upper_notification_height

    printed_y_pixel = 0
    printed_y_pixel_after = 0
    # now draw notification
    for i in range(len(notifications)):
        pass
        printed_y_pixel += printed_y_pixel_after
        this_notification_height = int(one_notification_max_height * notifications[i].display_visibility)
        printed_y_pixel_after = this_notification_height
        if this_notification_height <= 10: continue
        this_notification_width = int(one_notification_width * notifications[i].display_visibility)
        this_notification_start_x = (320 - this_notification_width) // 2
        this_notification_radius = int(this_notification_height // 2)
        this_notification_image_size = this_notification_height - 10
        if this_notification_image_size <= 0: continue
        # icon = cv.resize(black_screen, (this_notification_image_size, this_notification_image_size))
        # if notifications[i].icon == "hard_warning.png":
        #     icon = cv.resize(hard_warning_icon, (this_notification_image_size, this_notification_image_size))
        # elif notifications[i].icon == "warning.png":
        #     icon = cv.resize(warning_icon, (this_notification_image_size, this_notification_image_size))
        icon = get_icon(notifications[i].icon, this_notification_image_size)
        frame[
        notification_start_y + 5 + printed_y_pixel:notification_start_y + 5 + printed_y_pixel + this_notification_image_size,
        this_notification_start_x + 5:this_notification_start_x + 5 + this_notification_image_size] = icon
        string_able_pixel_width = this_notification_width - this_notification_image_size - 10
        string_able_pixel_height = this_notification_height - 10
        string_max_length = string_able_pixel_width // 10
        string = notifications[i].message
        if len(string) > string_max_length: string = string[:string_max_length] + "..."
        cv.putText(frame, string, (this_notification_start_x + this_notification_image_size + 10,
                                   notification_start_y + 5 + printed_y_pixel + this_notification_height // 2 + 5),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   (64, 64, 64), 1, cv.LINE_AA)

    return frame


def render_tensor_and_etc():
    pass
    global raw_screen
    new_frame = raw_screen
    # render tensor
    tensor_output = tensor_engine.tensor_output
    if tensor_output is not None:
        pass
        new_frame = render_tensors(tensor_output)
    # render etc
    # render notifications
    notifications_count = len(notification_engine.notifications)
    try:
        pass
        if key_engine.get_key("Notification Display Overlap").get("value"): new_frame = render_notifications(new_frame,
                                                                                                             notification_engine.notifications)
    except Exception as e:
        print("Error while rendering notifications.")
        print(e)
        pass
    # render fps
    if key_engine.get_key("ROSDisplayFPSEnable").get("value"):
        pass
        main_screen_fps = round(fps_engine.get_main_screen_fps(), 2)
        tensor_fps = round(fps_engine.get_tensor_fps(), 2)

        red = key_engine.get_key("ROSDisplayFPSColorRed").get("value")
        green = key_engine.get_key("ROSDisplayFPSColorGreen").get("value")
        blue = key_engine.get_key("ROSDisplayFPSColorBlue").get("value")

        # cv.putText(new_frame, "MS FPS: " + str(main_screen_fps), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
        #            (255, 255, 255), 1, cv.LINE_AA)
        # cv.putText(new_frame, " T FPS: " + str(tensor_fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
        #            1, cv.LINE_AA)
        cv.putText(new_frame, "MS FPS: " + str(main_screen_fps), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   (blue, green, red), 1, cv.LINE_AA)
        cv.putText(new_frame, " T FPS: " + str(tensor_fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (blue, green, red),
                   1, cv.LINE_AA)

    # render USSRegion
    if key_engine.get_key("USSRegionDisplayEnabled").get("value") and "boot.RUSS" in sys.modules:
        pass
        uss_region_start_x = key_engine.get_key("USSRegionStartX").get("value")
        uss_region_end_x = key_engine.get_key("USSRegionEndX").get("value")
        uss_region_start_y = key_engine.get_key("USSRegionStartY").get("value")
        uss_region_end_y = key_engine.get_key("USSRegionEndY").get("value")

        red = key_engine.get_key("USSRegionDisplayColorRed").get("value")
        green = key_engine.get_key("USSRegionDisplayColorGreen").get("value")
        blue = key_engine.get_key("USSRegionDisplayColorBlue").get("value")
        # cv.rectangle(new_frame, (uss_region_start_x, uss_region_start_y), (uss_region_end_x, uss_region_end_y),
        #              (208, 252, 92), 1)
        cv.rectangle(new_frame, (uss_region_start_x, uss_region_start_y), (uss_region_end_x, uss_region_end_y),
                     (blue, green, red), -1)
    global screen
    screen = new_frame
    return new_frame


def tick_screen():
    pass
    global kernel_panicked
    global screen
    if kernel_panicked:
        pass
        screen = kernel_panic_screen
    make_window()
    if key_engine.get_key("ROSARDisplayEnabled").get("value"):
        pass
        cv.imshow("ROS", make_ar_frame(screen))
    else:
        pass
        cv.imshow("ROS", screen)

    fps_engine.add_candidate_main_fps()
    if fps_engine.get_main_screen_fps() < 20 and notification_engine.get_notification(
            message="Low System FPS detected.") is None:
        pass
        notification_engine.add_notification("warning.png", "Low System FPS detected.",
                                             "시스템 FPS가 낮습니다. 늦은 반응에 대비 해주세요.")
    if fps_engine.get_tensor_fps() < 15 and notification_engine.get_notification(
            message="Low Tensor FPS detected.") is None:
        pass
        notification_engine.add_notification("warning.png", "Low Tensor FPS detected.", "텐서 FPS가 낮습니다. 늦은 반응에 대비 해주세요.")

    return


def set_tensor_input():
    pass
    global raw_screen
    raw_screen = get_320_320_frame(raw_screen)
    raw_data = cv.cvtColor(raw_screen, cv.COLOR_BGR2RGB)
    raw_data = np.expand_dims(raw_data, axis=0)
    tensor_engine.raw_data = raw_data
    return


def shutdown():
    pass
    print("Shutting down...")
    global camera
    notification_engine.add_notification("hard_warning.png", "Shutting down...", "종료 중...")
    # shutdown thread later
    tensor_engine.stop_process_frame()
    label_engine.erase_memory()
    color_engine.erase_memory()
    if "boot.RBluetooth" in sys.modules:
        pass
        bluetooth_engine.close()
    key_engine.save_keys()
    cv.destroyAllWindows()
    if "picamera2" in sys.modules:
        pass
        camera.stop()
    else:
        pass
        camera.release()
    notification_engine.close()
    tts_engine.shutdown()
    if "boot.RTaptic" in sys.modules:
        pass
        taptic_engine.shutdown()
        global taptic_command_thread_run
        taptic_command_thread_run = False
        global taptic_command_thread
        if taptic_command_thread is not None: taptic_command_thread.join()
    if "boot.RUSS" in sys.modules:
        pass
        ultrasonic_engine.shutdown()
    if "boot.RGPIO" in sys.modules:
        pass
        gpio_engine.shutdown()
    # time.sleep(2)
    current_threads = threading.enumerate()
    for thread in current_threads:
        pass
        if thread.name == "MainThread": continue
        print("Thread " + thread.name + " is in running.")
    if len(current_threads) > 1:
        pass
        print("There are still threads running.")
        print("Force shutdown.")
        os._exit(0)
    print("Shutdown complete.")
    exit(0)


def bluetooth_connected_callback():
    pass
    sound_engine.play("boot/res/alert.mp3")
    print("Bluetooth connected.")
    notification_engine.add_notification("warning.png", "Bluetooth connected.", "블루투스 연결되었습니다.")
    return


def bluetooth_signal_callback(data):
    pass
    global find_my_sounding_one_channel
    global find_my_keep_sounding_channel
    global find_my_notification
    if data == b"a":
        pass
        sound_engine.stop(find_my_sounding_one_channel)
        find_my_sounding_one_channel = sound_engine.play("boot/res/FindMy.mp3")
        notification_engine.add_notification("warning.png", "Find My is activated.", "나의 찾기가 활성화 되었습니다.")
    elif data == b"b":
        pass
        find_my_keep_sounding_channel = sound_engine.play("boot/res/FindMy_long.mp3", -1)
        find_my_notification = notification_engine.add_notification("warning.png", "Find My is activated.",
                                                                    "나의 찾기가 활성화 되었습니다.")
        find_my_notification.display_duration = 1000000
        # pass
    elif data == b"c":
        pass
        sound_engine.stop(find_my_keep_sounding_channel)
        find_my_notification.display_duration = 0
        # pass
    return


def boot_logo(started_ticks: float, target_ticks: float = 8.0):
    pass
    global screen
    # screen = black_screen
    # copy black screen to screen
    screen = np.zeros((320, 320, 3), np.uint8)
    screen = cv.cvtColor(screen, cv.COLOR_BGR2RGB)
    global splash_screen
    resized_splash_screen = cv.resize(splash_screen, (80, 80))
    screen[120:200, 120:200] = resized_splash_screen

    # cv.putText(screen, "ROS", (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    boot_progress = 0
    if started_ticks < target_ticks * 0.35:
        # boot_progress = started_ticks * 10.0
        boot_progress = started_ticks / (target_ticks * 0.35) * 30.0
        pass
    elif started_ticks < target_ticks * 0.6:
        # boot_progress = 30 + (started_ticks - 3) * 30.0
        # rage is 30 to 90
        boot_progress = 30 + (started_ticks - target_ticks * 0.35) / (target_ticks * 0.25) * 60.0
        pass
    elif started_ticks < target_ticks * 0.9:
        # boot_progress = 90 + 10 / 1.5 * (started_ticks - 5)
        # range is 90 to 100
        boot_progress = 90 + (started_ticks - target_ticks * 0.6) / (target_ticks * 0.3) * 10.0
        pass
    else:
        boot_progress = 100
        pass

    progress_bar_width_margin = 40
    progress_bar_height_margin = 10
    progress_bar_height = 5
    progress_bar_width = 320 - progress_bar_width_margin * 2
    progress_bar_corner_radius = progress_bar_height // 2
    # progress bar background
    cv.circle(screen, (progress_bar_width_margin + progress_bar_corner_radius,
                       320 - progress_bar_height_margin - progress_bar_corner_radius), progress_bar_corner_radius,
              (64, 64, 64), -1)
    cv.circle(screen, (320 - progress_bar_width_margin - progress_bar_corner_radius,
                       320 - progress_bar_height_margin - progress_bar_corner_radius), progress_bar_corner_radius,
              (64, 64, 64), -1)
    cv.rectangle(screen, (
        progress_bar_width_margin + progress_bar_corner_radius, 320 - progress_bar_height_margin - progress_bar_height),
                 (320 - progress_bar_width_margin - progress_bar_corner_radius, 320 - progress_bar_height_margin),
                 (64, 64, 64), -1)
    # progress bar
    cv.circle(screen, (progress_bar_width_margin + progress_bar_corner_radius,
                       320 - progress_bar_height_margin - progress_bar_corner_radius), progress_bar_corner_radius,
              (255, 255, 255), -1)
    cv.rectangle(screen, (
        progress_bar_width_margin + progress_bar_corner_radius, 320 - progress_bar_height_margin - progress_bar_height),
                 (
                     int(progress_bar_width_margin + progress_bar_corner_radius + (
                             320 - progress_bar_width_margin - progress_bar_corner_radius - progress_bar_width_margin - progress_bar_corner_radius) * (
                                 boot_progress / 100)), 320 - progress_bar_height_margin), (255, 255, 255), -1)
    cv.circle(screen, (int(progress_bar_width_margin + progress_bar_corner_radius + (
            320 - progress_bar_width_margin - progress_bar_corner_radius - progress_bar_width_margin - progress_bar_corner_radius) * (
                                   boot_progress / 100)),
                       320 - progress_bar_height_margin - progress_bar_corner_radius), progress_bar_corner_radius,
              (255, 255, 255), -1)
    return


def rotate_clockwise_90(frame):
    pass
    return cv.transpose(cv.flip(frame, 0))


def rotate_counterclockwise_90(frame):
    pass
    return cv.transpose(cv.flip(frame, 1))


def rotate_180(frame):
    pass
    return cv.flip(frame, -1)


def kernel_panic_check():
    pass
    if hard_warning_icon is None:
        pass
        return True
    if warning_icon is None:
        pass
        return True
    if black_screen is None:
        pass
        return True
    if kernel_panic_screen is None:
        pass
        return True
    if splash_screen is None:
        pass
        return True
    if raw_screen is None:
        pass
        return True
    if tensor_engine.model is None:
        pass
        return True
    return False


def distance_to_meter(distance: str):
    pass
    if distance is None: return None
    if distance == "": return None
    if distance.endswith("cm"):
        pass
        return float(distance[:-2]) / 100
    elif distance.endswith("m"):
        pass
        return float(distance[:-1])
    elif distance.endswith("km"):
        pass
        return float(distance[:-2]) * 1000
    elif distance.endswith("in"):
        pass
        return float(distance[:-2]) * 0.0254
    elif distance.endswith("ft"):
        pass
        return float(distance[:-2]) * 0.3048
    elif distance.endswith("yd"):
        pass
        return float(distance[:-2]) * 0.9144
    elif distance.endswith("mi"):
        pass
        return float(distance[:-2]) * 1609.34
    return None


def distance_taptic_feedback():
    pass
    if "boot.RTaptic" not in sys.modules: return
    if tensor_engine.tensor_output is None:
        pass
        taptic_engine.left_taptic.change_amp(0.0)
        taptic_engine.right_taptic.change_amp(0.0)
        return
    boxes, classes, scores, distance = tensor_engine.tensor_output
    if len(distance) == 0: return
    # distance is in any unit: cm, m, km, in, ft, yd, mi
    taptic_start_distance = key_engine.get_key("TapticFeedbackStartDistance").get("value")

    distance_in_meter = []

    for o in range(len(distance)):
        pass
        # if distance[o].endswith("cm") and float(
        #     distance[o][:-2]) < taptic_start_distance * 100: distance_in_meter.append(float(distance[o][:-2]) / 100)
        distance_in_meter.append(distance_to_meter(distance[o]))

    # min_distance = min(distance_in_meter)
    # if min_distance is None: return

    min_distance = distance_in_meter[0]
    for o in range(len(distance_in_meter)):
        pass
        if distance_in_meter[o] is None: continue
        min_distance = distance_in_meter[o]
        break
    # min_distance_index = 0
    for o in range(len(distance_in_meter)):
        pass
        if distance_in_meter[o] is None: continue
        if min_distance > distance_in_meter[o]: min_distance = distance_in_meter[o]

    if min_distance is None or min_distance > taptic_start_distance:
        pass
        taptic_engine.left_taptic.change_amp(0.0)
        taptic_engine.right_taptic.change_amp(0.0)
        return

    min_distance_index = distance_in_meter.index(min_distance)
    one_section = 320 / 3
    object_x_center = (boxes[min_distance_index][1] + boxes[min_distance_index][3]) / 2
    target_amp = 1.0 - min_distance / taptic_start_distance
    # change_amp
    if object_x_center < one_section:  # left
        pass
        taptic_engine.left_taptic.change_amp(target_amp)
    elif object_x_center < one_section * 2:  # center
        pass
        taptic_engine.left_taptic.change_amp(target_amp)
        taptic_engine.right_taptic.change_amp(target_amp)
    else:  # right
        pass
        taptic_engine.right_taptic.change_amp(target_amp)
    return


def taptic_feedback_loop():
    global taptic_command_thread_run
    while taptic_command_thread_run:
        pass
        distance_taptic_feedback()
        time.sleep(0.1)
    return


print("defs defined.")

print("preparing RKernel...")
tensor_engine.fps_engine = fps_engine
tensor_engine.calculate_distance_function = calculate_distance
notification_engine.tts_engine = tts_engine
notification_engine.tts_enabled = key_engine.get_key("Notification TTS Enabled").get("value")
if "boot.RBluetooth" in sys.modules:
    print("callback set.")
    bluetooth_engine.connected_callback = bluetooth_connected_callback
    bluetooth_engine.recv_callback = bluetooth_signal_callback
camera = get_camera()
sound_engine.overall_volume = key_engine.get_key("SoundVolume").get("value")
if "boot.RGPIOD" in sys.modules:
    pass
    if "boot.RTaptic" in sys.modules: taptic_engine.gpio_engine = gpio_engine
    if "boot.RUSS" in sys.modules: ultrasonic_engine.gpio_engine = gpio_engine

if "boot.RTaptic" in sys.modules:
    pass
    taptic_engine.init()

if "boot.RUSS" in sys.modules:
    pass
    ultrasonic_engine.init()

if "boot.RTaptic" in sys.modules:
    pass
    taptic_command_thread = threading.Thread(target=taptic_feedback_loop).start()

print("RKernel prepared.")

# set_tensor_input()
if key_engine.get_key("ROSBootChimeEnabled").get("value"):
    pass
    sound_engine.play("boot/res/StartUp.mp3")

started_time = time.time()
splash_display_time = key_engine.get_key("ROSSplashScreenTime").get("value")
while time.time() - started_time < splash_display_time:
    pass
    boot_logo(time.time() - started_time, splash_display_time)
    tick_screen()
    # debug
    # if hard_warning_icon is None:
    #     kernel_panicked = True
    kernel_panicked = kernel_panic_check()
    if cv.waitKey(1) & 0xFF == key_engine.get_key("ROSOffKey").get("value"):
        pass
        shutdown()

tts_engine.sound_engine = sound_engine
notification_engine.sound_engine = sound_engine
