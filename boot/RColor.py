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
