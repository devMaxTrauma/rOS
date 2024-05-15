import datetime

import cv2 as cv
import tensorflow as tf
import tensorflow_hub as hub


class Key:
    name = None
    value = None
    type = None
    comment = None

    def __init__(self, name, value, comment=None):
        self.name = name
        self.value = value
        self.type = type(value)
        self.comment = comment


class Color:
    class_label = None
    blue = None
    green = None
    red = None

    def __init__(self, class_label, red, green, blue):
        self.class_label = class_label
        self.blue = blue
        self.green = green
        self.red = red


class Label:
    label = None
    id = None
    average_width = None
    color = None

    def __init__(self, label, id_number, average_width):
        self.label = label
        self.id = id_number
        self.average_width = average_width
        self.color = get_color(label)


def get_label(label_id):
    for label in class_labels:
        if label.id == label_id:
            return label
    return "<E:???>"


def get_key(key_name):
    key_name = key_name.lower()
    for key in keys:
        if key.name == key_name:
            return key
    return None


def update_key(key_name, key_value, update_rky=False, key_coment=""):
    if update_rky:
        key_name = key_name.lower()
        copy_keys = []

        key_file = open("rKey.rKY", "r", encoding='UTF8')
        if key_file is None:
            make_error_message("Key file not found.", level="Error")
        for line in key_file:
            line = line.lower()
            copy_key_name, copy_key_type, copy_key_value, copy_key_coment = read_key_line(line)
            if copy_key_name == key_name:
                copy_key_value = key_value
                copy_key_coment = key_coment
            copy_keys.append(Key(copy_key_name, copy_key_value, comment=copy_key_coment))
        key_file.close()

        key_file = open("rKey.rKY", "w", encoding='UTF8')
        if key_file is None:
            make_error_message("Key file not found.", level="Error")
        for key in copy_keys:
            key_type_string = None
            if key.type == str:
                key_type_string = "string"
                key_file.write(
                    key.name + ": " + key_type_string + " = \"" + key.value.lower() + "\" <?>" + key.comment + " \n")
                continue
            elif key.type == int:
                key_type_string = "int"
            elif key.type == float:
                key_type_string = "float"
            elif key.type == bool:
                key_type_string = "bool"
            else:
                make_error_message("Key type not recognized.", level="Error")
            key_file.write(
                key.name + ": " + key_type_string + " = " + str(key.value).lower() + " <?>" + key.comment + "\n")

        key_file.close()
    else:
        key = get_key(key_name)
        key.value = key_value


def upload_key():
    print("Uploading keys...")
    key_file = open("rKey.rKY", "w", encoding='UTF8')
    for key in keys:
        key_type_string = None
        if key.type == str:
            key_type_string = "string"
            key_file.write(
                key.name + ": " + key_type_string + " = \"" + key.value.lower() + "\" <?>" + key.comment + "\n")
            continue
        elif key.type == int:
            key_type_string = "int"
        elif key.type == float:
            key_type_string = "float"
        elif key.type == bool:
            key_type_string = "bool"
        else:
            make_error_message("Key type not recognized.", level="Error")
        key_file.write(key.name + ": " + key_type_string + " = " + str(key.value).lower() + " <?>" + key.comment + "\n")
    key_file.close()
    print("Keys uploaded.")


keys = []
class_labels = []
class_colors = []
model = None
_positive_signs = ["true", "1", "yes", "y", "on", "enable", "enabled", "t", "ok", "good", "correct", "positive"]
_negative_signs = ["false", "0", "no", "n", "off", "disable", "disabled", "f", "bad", "wrong", "incorrect", "negative"]
prev_frame_time = datetime.datetime.now()
new_frame_time = datetime.datetime.now()


def boot():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("rKernel booting...")

    read_key()
    check_versions()
    load_model()
    load_colors()
    load_labels()

    print("rKernel boot finished.")


def shutdown():
    print("rKernel shutting down...")
    upload_key()
    print("rKernel shutdown finished.")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def read_key():
    print("rKernel load keys...")
    key_file = open("rKey.rKY", "r", encoding='UTF8')
    if key_file is None:
        make_error_message("Key file not found. Can't boot rKernel.", level="Fatal Error")
    else:
        print("Key file found.")

    for line in key_file:
        line = line.lower()
        key_name, key_type, key_value, key_comment = read_key_line(line)
        keys.append(Key(key_name, key_value, comment=key_comment))

    if get_key("ros_key_load_debug_log_enabled").value:
        max_key_name_length = len("Key Name")
        max_key_type_length = len("Key Type")
        max_key_value_length = len("Key Value")
        max_key_comment_length = len("Key Coment")
        for key in keys:
            if len(key.name) > max_key_name_length:
                max_key_name_length = len(key.name)
            if len(str(key.type)) > max_key_type_length:
                max_key_type_length = len(str(key.type))
            if len(str(key.value)) > max_key_value_length:
                max_key_value_length = len(str(key.value))
            if len(key.comment) > max_key_comment_length:
                max_key_comment_length = len(key.comment)

        print("-" * (max_key_name_length + max_key_type_length + max_key_value_length + max_key_comment_length + 4))
        print("Key Name".ljust(max_key_name_length), "Key Type".ljust(max_key_type_length),
              "Key Value".ljust(max_key_value_length), "Key Coment".ljust(max_key_comment_length) + "\n")

        for key in keys:
            print(key.name.ljust(max_key_name_length), str(key.type).ljust(max_key_type_length),
                  str(key.value).ljust(max_key_value_length), key.comment.ljust(max_key_comment_length))

        print("-" * (max_key_name_length + max_key_type_length + max_key_value_length + max_key_comment_length + 4))

    print("rKernel keys loaded.")


def read_key_line(line):
    key_name = line.split(":")[0].strip()
    key_type = line.split(":")[1].split("=")[0].strip()
    value = line.split("=")[1].strip().split("<?>")[0].strip()
    try:
        comment = line.split("<?>")[1].strip()
    except IndexError:
        comment = ""
    key_value = None

    if key_type == "string":
        value = value[1:-1]
        key_value = value
    elif key_type == "int":
        key_value = int(value)
    elif key_type == "float":
        key_value = float(value)
    elif key_type == "bool":
        if value in _positive_signs:
            key_value = True
        elif value in _negative_signs:
            key_value = False
        else:
            make_error_message("Not defined boolean value.", level="Error")
    else:
        make_error_message("Not defined key type", level="Error")

    return key_name, key_type, key_value, comment


def check_versions():
    print("Checking versions...")
    print("--------------------------------")

    print(get_key("ros_version").name + ":", get_key("ros_version").value)
    print(get_key("ros_key_version").name + ":", get_key("ros_key_version").value)
    print("opencv version:", cv.__version__)
    print("tensorflow version:", tf.__version__)
    print("tensorflow_hub version:", hub.__version__)

    print("--------------------------------")
    print("Versions checked.")


def load_model():
    print("Loading model...")
    if get_key("model_load_url").value is None:
        make_error_message("Model URL not found. Can't boot rKernel.", level="Fatal Error")

    if get_key("ros_model_load_debug_log_enabled").value:
        print("Model Name: ", get_key("model_name").value)
        print("Model URL: ", get_key("model_load_url").value)

    global model
    try:
        model = hub.load(get_key("model_load_url").value)
    except Exception as e:
        make_error_message(str(e), level="Fatal Error")
    if model is None:
        make_error_message("Model not found. Can't boot rKernel.", level="Fatal Error")
    print("Model loaded.")


def load_labels():
    print("Loading labels...")
    label_file = open(get_key("ros_class_labels_file_name").value, "r", encoding='UTF8')
    if label_file is None:
        make_error_message("Label file not found. Can't boot rKernel.", level="Fatal Error")
    else:
        print("Label file found.")

    max_label_length = len("Label")
    max_id_length = len("ID")
    max_average_width_length = len("Average Width")

    for line in label_file:
        label = line.split("=")[0].strip()
        id = line.split("=")[1].strip().split("%")[0].strip()
        average_width = line.split("%")[1].strip()
        if average_width == "":
            average_width = -1.0
        class_labels.append(Label(label, int(id), float(average_width)))

    label_file.close()

    if get_key("ros_class_labels_load_debug_log_enabled").value:
        print("-" * (max_label_length + max_id_length + max_average_width_length + 4))
        print("Label".ljust(max_label_length), "ID".ljust(max_id_length),
              "Average Width".ljust(max_average_width_length) + "\n")
        for i in range(len(class_labels)):
            print(class_labels[i].label.ljust(max_label_length), class_labels[i].id,
                  class_labels[i].average_width)

        print("-" * (max_label_length + max_id_length + max_average_width_length + 4))

    print("Labels loaded.")


def load_colors():
    print("Loading colors...")
    color_file = open(get_key("ros_class_colors_file_name").value, "r", encoding='UTF8')
    if color_file is None:
        make_error_message("Color file not found. Can't boot rKernel.", level="Fatal Error")
    else:
        print("Color file found.")
    max_class_name_length = len("Class Name")
    max_red_length = len("Red")
    max_green_length = len("Green")
    max_blue_length = len("Blue")
    for line in color_file:
        line = line.split("=")
        class_name = line[0].strip()
        hex_code = line[1].strip()
        red = int(hex_code[1:3], 16)
        green = int(hex_code[3:5], 16)
        blue = int(hex_code[5:7], 16)
        class_colors.append(Color(class_name, red, green, blue))
        if len(class_name) > max_class_name_length:
            max_class_name_length = len(class_name)
        if len(str(red)) > max_red_length:
            max_red_length = len(str(red))
        if len(str(green)) > max_green_length:
            max_green_length = len(str(green))
        if len(str(blue)) > max_blue_length:
            max_blue_length = len(str(blue))
    color_file.close()
    if get_key("ros_class_colors_load_debug_log_enabled").value:
        print("-" * (max_class_name_length + max_red_length + max_green_length + max_blue_length + 4))
        print("Class Name".ljust(max_class_name_length), "Red".ljust(max_red_length), "Green".ljust(max_green_length),
              "Blue".ljust(max_blue_length) + "\n")
        for color in class_colors:
            print(color.class_label.ljust(max_class_name_length), str(color.red).ljust(max_red_length),
                  str(color.green).ljust(max_green_length), str(color.blue).ljust(max_blue_length))
        print("-" * (max_class_name_length + max_red_length + max_green_length + max_blue_length + 4))
    print("Colors loaded.")


def get_color(class_label):
    for color in class_colors:
        if color.class_label == class_label:
            return color
    for color in class_colors:
        if color.class_label == "Else":
            return color


def make_error_message(message, level="Error"):
    if level == "Error":
        print(level + ": " + message)
        exit(1)
    elif level == "Warning":
        print(level + ": " + message)
        return
    elif level == "Key Error":
        print(level + ": " + message + " check the key name spelling and the key file.")
        return
    elif level == "Fatal Error":
        print(level + ": " + message)
        exit(1)
    else:
        print("Error: IDK what happened.")
        exit(666)


def get_fps():
    global prev_frame_time
    global new_frame_time
    prev_frame_time = new_frame_time
    new_frame_time = datetime.datetime.now()
    return 1 / (new_frame_time - prev_frame_time).total_seconds()


class Kernel:
    def __init__(self):
        boot()
