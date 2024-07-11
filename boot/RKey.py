keys = {}
positive_signs = ["True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "t", "T", "y", "Y"]
negative_signs = ["False", "false", "0", "no", "No", "NO", "off", "Off", "OFF", "f", "F", "n", "N"]


def read_key_line(key_line):
    global keys
    if key_line == "\n": return
    # key format: <name> name </> <type> str </> <value> hello, world! </> <comment> This is a comment. </>
    key_data = key_line.split("</>")
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
    elif key_type == "bool" and key_value in positive_signs:
        key_value = True
        key_type = type(key_value)
    elif key_type == "bool" and key_value in negative_signs:
        key_value = False
        key_type = type(key_value)
    elif key_type == "bool":
        print("Warning!: Invalid boolean value for key: " + key_name + ".")
        key_value = None
    elif key_type == "str":
        key_type = type(key_value)
    else:
        print("Warning!: Invalid key type for key: " + key_name + ".")
        key_value = None

    keys[key_name] = {"type": key_type, "value": key_value, "comment": key_comment}


def __load_keys__():
    global keys
    try:
        r_key_file = open("boot/res/RKey.RKY", "r", encoding="utf-8")
        key_list = r_key_file.readlines()
        r_key_file.close()
        for one_key in key_list: read_key_line(one_key)
    except FileNotFoundError:
        print("RKey.RKY not found.")
        return
    except Exception as e:
        print("Error loading keys.")
        print(e)
        exit(999)

    if keys["BootDebugLogOn"].get("value"):
        print("\nDebug(BootDebugLogOn): Loaded keys are as follows: ")
        __debug_log_printer__()


def get_key(key_name):
    global keys
    if key_name in keys:
        return keys[key_name]
    else:
        return None


def set_key(key_name, key_value):
    global keys
    if key_name in keys:
        keys[key_name]["value"] = key_value
        save_keys()
        if keys["RKeySetDebugLogOn"].get("value"): print(
            "\nDebug(RKeySetDebugLogOn): Key " + key_name + " set to " + str(key_value) + ".")
        return True
    else:
        return False


def save_key_line(key_name, file):
    global keys
    key_type = keys[key_name]["type"]
    key_value = str(keys[key_name]["value"])
    key_comment = keys[key_name]["comment"]
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

    file.write(
        "<name> " + key_name + " </> <type> " + key_type + " </> <value> " + key_value + " </> <comment> " + key_comment + " </>\n")


def save_keys():
    global keys
    try:
        r_key_file = open("boot/res/RKey.RKY", "w", encoding="utf-8")
        for key_name in keys: save_key_line(key_name, r_key_file)
        r_key_file.close()
    except Exception as e:
        print("Error saving keys.")
        print(e)
        exit(999)

    if keys["RKeySaveDebugLogOn"].get("value"):
        print("\nDebug(RKeySaveDebugLogOn): Saved keys are as follows: ")
        __debug_log_printer__()
    return True


def __debug_log_printer__():
    global keys
    name_max_len = len("Name")
    type_max_len = len("Type")
    value_max_len = len("Value")
    comment_max_len = len("Comment")

    for key_name in keys:
        name_max_len = max(name_max_len, len(key_name))
        type_max_len = max(type_max_len, len(str(keys[key_name]["type"])))
        value_max_len = max(value_max_len, len(str(keys[key_name]["value"])))
        comment_max_len = max(comment_max_len, len(keys[key_name]["comment"]))

    print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
            value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")
    print("| Name" + " " * (name_max_len - 4) + " | Type" + " " * (type_max_len - 4) + " | Value" + " " * (
            value_max_len - 5) + " | Comment" + " " * (comment_max_len - 7) + " |")
    print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
            value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")
    for key_name in keys:
        print("| " + key_name + " " * (name_max_len - len(key_name)) + " | " + str(
            keys[key_name]["type"]) + " " * (
                      type_max_len - len(str(keys[key_name]["type"]))) + " | " + str(
            keys[key_name]["value"]) + " " * (value_max_len - len(str(keys[key_name]["value"]))) + " | " +
              keys[key_name]["comment"] + " " * (comment_max_len - len(keys[key_name]["comment"])) + " |")
        print("+" + "-" * (name_max_len + 2) + "+" + "-" * (type_max_len + 2) + "+" + "-" * (
                value_max_len + 2) + "+" + "-" * (comment_max_len + 2) + "+")


print("RKey engine: loading keys...")
__load_keys__()
print("RKey engine: keys loaded.")
