class RKernel:
    import time
    import tensorflow as tf
    import cv2 as cv

    def __init__(self):
        self.__boot__()

    def __boot__(self):
        print("rKernel booting up...")
        self.splash_screen = self.cv.imread("ROS_SPLASH.png")
        self.__load_sound__()
        self.__load_key__()
        self.__load_model__()
        self.key_engine.set_key("ROSIsOn", True)
        print("rKernel booted up.")

    def __load_key__(self):
        print("Loading key engine...")
        self.key_engine = RKey()
        print("Key engine loaded.")

    def __load_sound__(self):
        print("Loading sound engine...")
        self.sound_engine = RSound()
        print("Sound engine loaded.")

    def __load_model__(self):
        print("Loading model...")
        self.model = self.tf.lite.Interpreter(model_path='yolov5sdynm_range.tflite')
        self.model.allocate_tensors()
        self.model_input_details = self.model.get_input_details()
        self.model_output_details = self.model.get_output_details()
        print("Model loaded.")

    def shutdown(self):
        print("Shutting down rKernel...")
        self.cv.destroyAllWindows()
        self.sound_engine.pygame.quit()
        self.key_engine.set_key("ROSIsOn", False)
        print("rKernel shut down.")

    def process_frame(self, frame):
        if self.model is None:
            return None
        input_shape = self.model_input_details[0]['shape']
        frame = self.cv.resize(frame, (input_shape[1], input_shape[2]))
        frame = self.cv.cvtColor(frame, self.cv.COLOR_BGR2RGB)
        frame = self.tf.convert_to_tensor(frame)
        # tensor value of float32
        frame = self.tf.cast(frame, self.tf.float32)
        frame = frame / 255.0
        frame = frame.numpy()
        frame = frame.reshape(input_shape)
        self.model.set_tensor(self.model_input_details[0]['index'], frame)
        self.model.invoke()
        output_data = self.model.get_tensor(self.model_output_details[0]['index'])
        return output_data


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
                self.keys[key_name]["value"]) + " " * (
                          value_max_len - len(str(self.keys[key_name]["value"]))) + " | " + self.keys[key_name][
                      "comment"] + " " * (comment_max_len - len(self.keys[key_name]["comment"])) + " |")
        print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
                value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")


class RSound:
    import pygame
    import threading

    channels = []

    def __init__(self):
        self.pygame.init()
        self.threading.Thread(target=self._running).start()
        self.play("startup.wav")

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
