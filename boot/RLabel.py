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
