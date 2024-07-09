# import socket

class RKernel:

    def __init__(self):
        self.__boot__()
        if self.key_engine.get_key("ROSBootChimeEnabled").get("value"):
            self.sound_engine.play("startup.wav")
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
            # prev version
            # left_eye_screen = frame  # copy left eye
            # right_eye_screen = frame  # copy right eye
            # usable_width_per_eye_in_meter = (user_eye_distance / 2) - 0.005  # meter
            # usable_width_per_eye_in_pixel = int(usable_width_per_eye_in_meter * ar_ppi * 39.3701)
            # usable_width_per_eye_in_pixel = min(usable_width_per_eye_in_pixel, 320)
            # print("usable pixel:", usable_width_per_eye_in_pixel)
            #
            # left_eye_screen = left_eye_screen[:, 0:usable_width_per_eye_in_pixel]
            # right_eye_screen = right_eye_screen[:, 320 - usable_width_per_eye_in_pixel:]
            #
            # ar_screen[eye_start_y:eye_start_y + 320,
            # left_eye_start_x:left_eye_start_x + usable_width_per_eye_in_pixel] = left_eye_screen
            # ar_screen[eye_start_y:eye_start_y + 320,
            # right_eye_start_x + 320 - usable_width_per_eye_in_pixel:right_eye_start_x + 320] = right_eye_screen

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


class RKey:
    keys = {}
    positive_signs = ["True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "t", "T", "y", "Y"]
    negative_signs = ["False", "false", "0", "no", "No", "NO", "off", "Off", "OFF", "f", "F", "n", "N"]

    def __init__(self):
        print("RKey engine: loading keys...")
        self.__load_keys__()
        print("RKey engine: keys loaded.")

    def __load_keys__(self):
        try:
            r_key_file = open("RKey.RKY", "r", encoding="utf-8")
            key_list = r_key_file.readlines()
            r_key_file.close()
            for one_key in key_list:
                if one_key == "\n":
                    continue
                # key format: <name> name </> <type> str </> <value> hello, world! </> <comment> This is a comment. </>
                key_data = one_key.split("</>")
                key_name = key_data[0].split("<name>")[1].strip()
                key_type = key_data[1].split("<type>")[1].strip()
                key_value = key_data[2].split("<value>")[1].strip()
                key_comment = key_data[3].split("<comment>")[1].strip()
                if key_type == "int":
                    key_value = int(key_value)
                    key_type = type(key_value)
                elif key_type == "float":
                    key_value = float(key_value)
                    key_type = type(key_value)
                elif key_type == "bool":
                    if key_value in self.positive_signs:
                        key_value = True
                        key_type = type(key_value)
                    elif key_value in self.negative_signs:
                        key_value = False
                        key_type = type(key_value)
                    else:
                        print("Warning!: Invalid boolean value for key: " + key_name + ".")
                        key_value = None
                elif key_type == "str":
                    key_type = type(key_value)
                else:
                    print("Warning!: Invalid key type for key: " + key_name + ".")
                    key_value = None

                self.keys[key_name] = {"type": key_type, "value": key_value, "comment": key_comment}

        except FileNotFoundError:
            print("RKey.RKY not found.")
            return
        except Exception as e:
            print("Error loading keys.")
            print(e)
            exit(999)

        if self.keys["BootDebugLogOn"].get("value"):
            print("\nDebug(BootDebugLogOn): Loaded keys are as follows: ")
            self.__debug_log_printer__()

    def get_key(self, key_name):
        if key_name in self.keys:
            return self.keys[key_name]
        else:
            return None

    def set_key(self, key_name, key_value):
        if key_name in self.keys:
            self.keys[key_name]["value"] = key_value
            self.save_keys()
            if self.keys["RKeySetDebugLogOn"].get("value"):
                print("\nDebug(RKeySetDebugLogOn): Key " + key_name + " set to " + str(key_value) + ".")
            return True
        else:
            return False

    def save_keys(self):
        try:
            r_key_file = open("RKey.RKY", "w", encoding="utf-8")
            for key_name in self.keys:
                key_type = self.keys[key_name]["type"]
                key_value = str(self.keys[key_name]["value"])
                key_comment = self.keys[key_name]["comment"]
                if key_type == int:
                    key_type = "int"
                elif key_type == float:
                    key_type = "float"
                elif key_type == bool:
                    key_type = "bool"
                elif key_type == str:
                    key_type = "str"
                else:
                    print("Warning!: Invalid key type for key: " + key_name + ".")
                    key_type = "ERROR_HERE!!!"

                r_key_file.write(
                    "<name> " + key_name + " </> <type> " + key_type + " </> <value> " + key_value + " </> <comment> " + key_comment + " </>\n")

            r_key_file.close()
        except Exception as e:
            print("Error saving keys.")
            print(e)
            exit(999)

        if self.keys["RKeySaveDebugLogOn"].get("value"):
            print("\nDebug(RKeySaveDebugLogOn): Saved keys are as follows: ")
            self.__debug_log_printer__()
        return True

    def __debug_log_printer__(self):
        name_max_len = len("Name")
        type_max_len = len("Type")
        value_max_len = len("Value")
        comment_max_len = len("Comment")

        for key_name in self.keys:
            name_max_len = max(name_max_len, len(key_name))
            type_max_len = max(type_max_len, len(str(self.keys[key_name]["type"])))
            value_max_len = max(value_max_len, len(str(self.keys[key_name]["value"])))
            comment_max_len = max(comment_max_len, len(self.keys[key_name]["comment"]))

        print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
                value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")
        print("| Name" + " " * (name_max_len - 4) + " | Type" + " " * (type_max_len - 4) + " | Value" + " " * (
                value_max_len - 5) + " | Comment" + " " * (comment_max_len - 7) + " |")
        print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
                value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")
        for key_name in self.keys:
            print("| " + key_name + " " * (name_max_len - len(key_name)) + " | " + str(
                self.keys[key_name]["type"]) + " " * (
                          type_max_len - len(str(self.keys[key_name]["type"]))) + " | " + str(
                self.keys[key_name]["value"]) + " " * (value_max_len - len(str(self.keys[key_name]["value"]))) + " | " +
                  self.keys[key_name]["comment"] + " " * (comment_max_len - len(self.keys[key_name]["comment"])) + " |")
        print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
                value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")


class RSound:
    import pygame
    import threading

    channels = []

    def __init__(self):
        self.pygame.init()
        self.threading.Thread(target=self._running).start()
        # self.play("startup.wav")

    def _running(self):
        while True:
            for channel in self.channels:
                if not channel.get_busy():
                    self.channels.remove(channel)
            self.pygame.time.Clock().tick(10)
            if not self.channels:
                break

    def play(self, sound_path):
        channel = self.pygame.mixer.Channel(len(self.channels))
        sound = self.pygame.mixer.Sound(sound_path)
        channel.play(sound)
        self.channels.append(channel)
        if self.threading.active_count() == 1:
            self.threading.Thread(target=self._running).start()
        return channel

    def stop(self, channel):
        channel.stop()
        self.channels.remove(channel)


class RLabel:
    def __init__(self):
        self.labels = {}
        self.__load_labels__()

    def __load_labels__(self):
        try:
            r_label_file = open("RClassLabelEn.RCL", "r", encoding="utf-8")
            label_list = r_label_file.readlines()
            r_label_file.close()
            for one_label in label_list:
                if one_label == "\n":
                    continue
                # label format: label = index % average_width
                label_data = one_label.split("=")
                label_value = label_data[0].strip()
                label_data = label_data[1].split("%")
                label_index = int(label_data[0].strip())
                if len(label_data[1].strip()) > 0:
                    label_average_width = float(label_data[1].strip())
                else:
                    label_average_width = -1.0
                self.labels[label_index] = {"value": label_value, "average_width": label_average_width}
        except FileNotFoundError:
            print("RClassLabelEn.RCL not found.")
            return
        except Exception as e:
            print("Error loading labels.")
            print(e)
            exit(999)

        label_max_len = len("Label")
        index_max_len = len("Index")
        average_width_max_len = len("Average Width")
        for label_index in self.labels:
            label_max_len = max(label_max_len, len(self.labels[label_index]["value"]))
            index_max_len = max(index_max_len, len(str(label_index)))
            if self.labels[label_index]["average_width"] == -1.0:
                pass
            else:
                average_width_max_len = max(average_width_max_len, len(str(self.labels[label_index]["average_width"])))

        print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
                average_width_max_len + 2) + "+")
        print("| Label" + " " * (label_max_len - 5) + " | Index" + " " * (
                index_max_len - 5) + " | Average Width" + " " * (average_width_max_len - 12) + " |")
        print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
                average_width_max_len + 2) + "+")
        for label_index in self.labels:
            average_width_specific = self.labels[label_index]["average_width"]
            if average_width_specific == -1.0:
                average_width_specific = ""
            print("| " + self.labels[label_index]["value"] + " " * (
                    label_max_len - len(self.labels[label_index]["value"])) + " | " + str(label_index) + " " * (
                          index_max_len - len(str(label_index))) + " | " + str(
                average_width_specific) + " " * (
                          average_width_max_len - len(str(average_width_specific))) + " |")
        print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
                average_width_max_len + 2) + "+")

    def get_label(self, label_index):
        if label_index in self.labels:
            return self.labels[label_index]
        else:
            return None

    def erase_memory(self):
        print("Erasing label memory...")
        self.labels = {}
        print("Label memory erased.")


class RColor:
    def __init__(self):
        self.colors = {}
        self.__load_colors__()

    def __load_colors__(self):
        try:
            r_color_file = open("RClassColor.RCC", "r", encoding="utf-8")
            color_list = r_color_file.readlines()
            r_color_file.close()
            for one_color in color_list:
                if one_color == "\n":
                    continue
                # color format: label_name = #RRGGBB
                color_data = one_color.split("=")
                color_value = color_data[0].strip()
                color_data = color_data[1].strip()
                color_r = int(color_data[1:3], 16)
                color_g = int(color_data[3:5], 16)
                color_b = int(color_data[5:7], 16)
                # rgb2bgr
                self.colors[color_value] = (color_b, color_g, color_r)
        except FileNotFoundError:
            print("RColor.RCL not found.")
            return
        except Exception as e:
            print("Error loading colors.")
            print(e)
            exit(999)

        label_name_max_len = len("Label Name")
        red_max_len = len("Red")
        green_max_len = len("Green")
        blue_max_len = len("Blue")
        for color_value in self.colors:
            label_name_max_len = max(label_name_max_len, len(color_value))
            red_max_len = max(red_max_len, len(str(self.colors[color_value][2])))
            green_max_len = max(green_max_len, len(str(self.colors[color_value][1])))
            blue_max_len = max(blue_max_len, len(str(self.colors[color_value][0])))
        print("+" + "-" * (label_name_max_len + 2) + "+" + "-" * (red_max_len + 2) + "+" + "-" * (
                green_max_len + 2) + "+" + "-" * (blue_max_len + 2) + "+")
        print(
            "| Label Name" + " " * (label_name_max_len - 10) + " | Red" + " " * (red_max_len - 3) + " | Green" + " " * (
                    green_max_len - 5) + " | Blue" + " " * (blue_max_len - 4) + " |")
        print("+" + "-" * (label_name_max_len + 2) + "+" + "-" * (red_max_len + 2) + "+" + "-" * (
                green_max_len + 2) + "+" + "-" * (blue_max_len + 2) + "+")
        for color_value in self.colors:
            print("| " + color_value + " " * (label_name_max_len - len(color_value)) + " | " + str(
                self.colors[color_value][2]) + " " * (
                          red_max_len - len(str(self.colors[color_value][2]))) + " | " + str(
                self.colors[color_value][1]) + " " * (
                          green_max_len - len(str(self.colors[color_value][1]))) + " | " + str(
                self.colors[color_value][0]) + " " * (blue_max_len - len(str(self.colors[color_value][0]))) + " |")
        print("+" + "-" * (label_name_max_len + 2) + "+" + "-" * (red_max_len + 2) + "+" + "-" * (
                green_max_len + 2) + "+" + "-" * (blue_max_len + 2) + "+")

    def get_color(self, color_value):
        if color_value in self.colors:
            return self.colors[color_value]
        else:
            return self.colors["Else"]

    def erase_memory(self):
        print("Erasing color memory...")
        self.colors = {}
        print("Color memory erased.")


class RSocket:
    # this code is for socket transfer
    import socket
    import threading

    def __init__(self, ip, port):
        print("Socket connecting to " + ip + ":" + str(port) + "...")
        self.ip = ip
        self.port = port
        self.socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        print("Socket created.")
        self.socket.bind((self.ip, self.port))
        print("Socket connected to " + self.ip + ":" + str(self.port) + ".")
        self.socket.listen(1)
        rkey = RKey()
        self.socket.settimeout(rkey.get_key("SLDConnectTimeout").get("value"))
        print("Socket listening...")

        while True:
            try:
                print("looped fuck")
                self.sld_socket, self.sld_address = self.socket.accept()
                print("Connected to " + str(self.sld_address) + ".")
                self.sld_rx_thread = self.threading.Thread(target=self.socket_rx_thread, args=(self.sld_socket,))
                self.sld_rx_thread.start()
                if self.sld_socket:
                    break
            except socket.timeout:
                print("timeout")
                break

    def socket_rx_thread(self, sld_socket):
        try:
            while True:
                data = sld_socket.recv(1024)
                if not data:  # if data is empty
                    continue
                elif data == b"exit":  # if data is "exit"
                    break
                print("Received: " + str(data))
        except Exception as e:
            print("Error in socket_rx_thread.")
            print(e)
        finally:
            sld_socket.close()
            print("Socket closed.")

    def send(self, data):
        self.socket.send(data)

    def receive(self):
        return self.socket.recv(1024)

    def close(self):
        self.sld_rx_thread.join()
        self.socket.close()
        print("Socket closed.")


class RBluetooth:
    def __init__(self):
        self.sound_engine = RSound()
        self.client_info = None
        self.client_sock = None
        self.bluetooth_rx_thread = None
        self.bluetooth_connected = False
        self.bluetooth = __import__("bluetooth")
        self.threading = __import__("threading")
        self.server_sock = self.bluetooth.BluetoothSocket(self.bluetooth.RFCOMM)
        self.server_sock.bind(("", self.bluetooth.PORT_ANY))
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
        self.service_name = "FindMy"

        try:
            self.bluetooth.advertise_service(self.server_sock, self.service_name,
                                            service_id=self.uuid,
                                            service_classes=[self.uuid, self.bluetooth.SERIAL_PORT_CLASS],
                                            profiles=[self.bluetooth.SERIAL_PORT_PROFILE])
        except Exception as e:
            print("Error in bluetooth advertise_service.")

        self.threading.Thread(target=self.bluetooth_connect_try).start()
        print("now you can connect to the bluetooth.")

    def bluetooth_connect_try(self):
        while True:
            try:
                if self.bluetooth_connected:
                    import time
                    time.sleep(1)
                    continue
                self.server_sock.settimeout(10)
                self.client_sock, self.client_info = self.server_sock.accept()
                print("Accepted connection from", self.client_info)
                self.bluetooth_rx_thread = self.threading.Thread(target=self.bluetooth_rx_interrupt, args=(self.client_sock,)).start()

                if self.client_sock:
                    print("connected.")
                    self.bluetooth_connected = True
                    break
                pass
            except Exception as e:
                if self.bluetooth_rx_thread is not None:
                    self.client_sock.close()
                    self.bluetooth_rx_thread.join()
                    self.bluetooth_rx_thread = None
                    pass
                print("RBluetooth: Error: Error in bluetooth connection.")
                print(e)
                print("RBluetooth: retrying...")
                pass
            pass

    def bluetooth_rx_interrupt(self, client_sock):
        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                print("Received: " + str(data))

                if data == b"a":
                    self.sound_engine.play("FindMy.mp3")
                    pass
        except Exception as e:
            print("Error in rx_interrupt.")
            print(e)
            self.bluetooth_connected = False
            pass

    def close(self):
        self.sound_engine.pygame.quit()
        if self.bluetooth_rx_thread is not None:
            self.client_sock.close()
            self.bluetooth_rx_thread.join()
            self.bluetooth_rx_thread = None
            pass
        self.server_sock.close()
        print("Bluetooth closed.")


    # def __init__(self):
    #     self.bluetooth = __import__("bluetooth")
    #     self.threading = __import__("threading")
    #     self.sound_engine = RSound()
    #     self.server_sock = self.bluetooth.BluetoothSocket(self.bluetooth.RFCOMM)
    #     self.server_sock.bind(("", self.bluetooth.PORT_ANY))
    #     self.server_sock.listen(1)
    #
    #     self.port = self.server_sock.getsockname()[1]
    #     self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
    #     self.service_name = "FindMy"
    #     try:
    #         bluetooth.advertise_service(self.server_sock, self.service_name,
    #                                     service_id=self.uuid,
    #                                     service_classes=[self.uuid, self.bluetooth.SERIAL_PORT_CLASS],
    #                                     profiles=[self.bluetooth.SERIAL_PORT_PROFILE])
    #     except Exception as e:
    #         print("Error in bluetooth advertise_service.")
    #     print("Waiting for connection on RFCOMM channel", self.port)
    #
    #     self.server_sock.settimeout(10)
    #     try:
    #         while True:
    #             self.client_sock, self.client_info = self.server_sock.accept()
    #             print("Accepted connection from", self.client_info)
    #             self.rx_thread = self.threading.Thread(target=self.rx_interrupt, args=(self.client_sock,)).start()
    #
    #             if self.client_sock:
    #                 print("connected.")
    #                 break
    #         pass
    #     except Exception as e:
    #         print("Error in bluetooth connection.")
    #         print(e)
    #         pass
    #
    # def rx_interrupt(self, client_sock):
    #     try:
    #         while True:
    #             data = client_sock.recv(1024)
    #             if not data:
    #                 break
    #             print("Received: " + str(data))
    #
    #             if data == b"a":
    #                 print("we did it! mother fucking shit!!!!!")
    #                 self.sound_engine.play("FindMy.mp3")
    #                 pass
    #             else:
    #                 print("not as expected, but something is going on")
    #                 print(str(data))
    #     except Exception as e:
    #         print("Error in rx_interrupt.")
    #         print(e)
    #         pass
    #     finally:
    #         client_sock.close()
    #         print("Bluetooth closed.")
    #         pass
    #     pass
    #
    # def close(self):
    #     # self.rx_thread.join()
    #     self.server_sock.close()
    #     self.sound_engine.pygame.quit()
    #     print("Bluetooth closed.")
    #     pass
