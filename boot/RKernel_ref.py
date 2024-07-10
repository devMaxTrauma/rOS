def __init__(self):
    self.__boot__()
    if self.key_engine.get_key("ROSBootChimeEnabled").get("value"):
        self.sound_engine.play("StartUp.mp3")
        pass
    else:
        pass


def __boot__(self):
    print("rKernel booting up...")
    self.__load_key__()
    self.__load_imports__()
    print("imported")
    self.splash_screen = self.cv.imread("ROS_SPLASH.png")
    self.__load_sound__()
    self.__load_label__()
    self.__load_color__()
    self.__load_model__()
    # self.__load_socket__()
    self.__load_bluetooth__()
    self.key_engine.set_key("ROSIsOn", True)
    print("rKernel booted up.")
    pass


def __load_imports__(self):
    print("Loading imports...")
    self.tf = __import__("tensorflow")
    self.cv = __import__("cv2")
    self.np = __import__("numpy")
    self.time = __import__("time")
    if self.key_engine.get_key("ROSRunningDevice").get("value") == "raspberry pi":
        print("ROS is running on raspberry pi. So importing Picamera2...")
        self.picamera2 = __import__("picamera2")
        print("Picamera2 imported.")
    print("Imports loaded.")

    print("checking versions")
    print("tensorflow version:", self.tf.__version__)
    print("opencv version:", self.cv.__version__)
    print("numpy version:", self.np.__version__)
    print("versions checked.")
    print("ROS is running on " + self.key_engine.get_key("ROSRunningDevice").get("value"))
    print("Camera Device: " + self.key_engine.get_key("CameraDevice").get("value"))
    print("ROS Version: " + self.key_engine.get_key("ROSVersion").get("value"))
    pass


def __load_key__(self):
    print("Loading key engine...")
    self.key_engine = RKey()
    print("Key engine loaded.")


def __load_sound__(self):
    print("Loading sound engine...")
    self.sound_engine = RSound()
    print("Sound engine loaded.")


def __load_label__(self):
    print("Loading label engine...")
    self.label_engine = RLabel()
    print("Label engine loaded.")


def __load_color__(self):
    print("Loading color engine...")
    self.color_engine = RColor()
    print("Color engine loaded.")


def __load_model__(self):
    print("Loading model...")
    self.model = self.tf.lite.Interpreter(model_path='model.tflite')
    self.model.allocate_tensors()
    self.model_input_details = self.model.get_input_details()
    self.model_output_details = self.model.get_output_details()
    print("Model loaded.")


def __load_socket__(self):
    # this code is abandoned haha
    print("Loading socket...")
    ip = self.key_engine.get_key("SLDDeviceIP").get("value")
    port = self.key_engine.get_key("SLDDevicePort").get("value")
    self.socket_engine = RSocket(ip, port)
    print("Socket loaded.")


def __load_bluetooth__(self):
    if self.key_engine.get_key("ROSRunningDevice").get("value") != "raspberry pi":
        return
    print("Loading bluetooth...")
    self.bluetooth_engine = RBluetooth()
    print("Bluetooth loaded.")


def shutdown(self):
    print("Shutting down rKernel...")
    self.cv.destroyAllWindows()
    self.sound_engine.pygame.quit()
    self.label_engine.erase_memory()
    self.color_engine.erase_memory()
    # self.socket_engine.close()
    if self.key_engine.get_key("ROSRunningDevice").get("value") == "raspberry pi":
        self.bluetooth_engine.close()
        pass
    self.key_engine.set_key("ROSIsOn", False)
    print("rKernel is safe to shut down.")
    print("rKernel shut down.")


def process_frame(self, frame):
    if self.model is None:
        return None
    frame = self.cv.cvtColor(frame, self.cv.COLOR_BGR2RGB)
    frame = self.np.expand_dims(frame, axis=0)
    self.model.set_tensor(self.model_input_details[0]['index'], frame)
    self.model.invoke()


def calculate_distance(self, object_average_width, box_width_pixel):
    distance_calculate_constance = self.key_engine.get_key("ROSObjectDistanceCalculateConstantDefault").get("value")
    if self.key_engine.get_key("CameraDevice").get("value") == "raspberry pi":
        distance_calculate_constance = self.key_engine.get_key("ROSObjectDistanceCalculateConstantRaspberryPi").get(
            "value")
        pass
    elif self.key_engine.get_key("CameraDevice").get("value") == "macbook pro":
        distance_calculate_constance = self.key_engine.get_key("ROSObjectDistanceCalculateConstantMacBookPro").get(
            "value")
        pass
    elif self.key_engine.get_key("CameraDevice").get("value") == "iphone":
        distance_calculate_constance = self.key_engine.get_key("ROSObjectDistanceCalculateConstantIphone").get(
            "value")
        pass
    else:
        print("Warning!: Invalid camera device. Using default constant.")
        pass

    if object_average_width == -1.0:
        return str("N/A")

    distance_in_meter = object_average_width / (box_width_pixel / distance_calculate_constance)
    unit = self.key_engine.get_key("DistanceUnit").get("value")
    if unit == "SI":
        if distance_in_meter < 1:
            return str(round(distance_in_meter * 100, 2)) + "cm"
        elif distance_in_meter < 1000:
            return str(round(distance_in_meter, 2)) + "m"
        else:
            return str(round(distance_in_meter / 1000, 2)) + "km"
        pass

    elif unit == "US":
        if distance_in_meter < 0.3048:
            return str(round(distance_in_meter * 39.3701, 2)) + "in"
        elif distance_in_meter < 0.9144:
            return str(round(distance_in_meter * 3.28084, 2)) + "ft"
        elif distance_in_meter < 1609.34:
            return str(round(distance_in_meter * 1.09361, 2)) + "yd"
        else:
            return str(round(distance_in_meter / 1609.34, 2)) + "mi"
        pass


def make_ar_frame(self, frame):
    # make sure that input frame is 320x320
    if frame.shape[0] != 320 or frame.shape[1] != 320:
        target_width = 320
        target_height = 320
        aspect_ratio = float(target_height) / frame.shape[0]
        dsize = (int(frame.shape[1] * aspect_ratio), target_height)
        new_frame = self.cv.resize(frame, dsize)
        new_frame = new_frame[:,
                    new_frame.shape[1] // 2 - target_width // 2: new_frame.shape[1] // 2 + target_width // 2]
        frame = new_frame
        pass
    # frame input resolution: 320 320
    ar_width = self.key_engine.get_key("ARDisplayWidth").get("value")
    ar_height = self.key_engine.get_key("ARDisplayHeight").get("value")
    ar_ppi = self.key_engine.get_key("ARDisplayPPI").get("value")
    user_eye_distance = self.key_engine.get_key("AREyeDistance").get("value")  # meter

    ar_screen = self.np.zeros((ar_height, ar_width, 3), self.np.uint8)
    ar_screen = self.cv.cvtColor(ar_screen, self.cv.COLOR_BGR2RGB)

    eye_distance_to_inch = user_eye_distance * 39.3701
    eye_distance_to_pixel = int(eye_distance_to_inch * ar_ppi)

    left_eye_center_x = (ar_width // 2) - (eye_distance_to_pixel // 2)
    right_eye_center_x = (ar_width // 2) + (eye_distance_to_pixel // 2)
    eye_center_y = ar_height // 2

    left_eye_start_x = left_eye_center_x - (320 // 2)
    right_eye_start_x = right_eye_center_x - (320 // 2)
    eye_start_y = eye_center_y - (320 // 2)

    if self.key_engine.get_key("ARMode").get("value") == "both eye":
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

    elif self.key_engine.get_key("ARMode").get("value") == "one eye":
        preferred_eye = self.key_engine.get_key("ARPreferredEye").get("value")
        if preferred_eye == "left":  # copy left eye
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

        elif preferred_eye == "right":  # copy right eye
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
