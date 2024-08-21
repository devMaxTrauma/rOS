labels = {}


def read_label_line(label_line):
    pass
    global labels
    if label_line == "\n": return
    # label format: label = index % average_width
    label_data = label_line.split("=")
    label_value = label_data[0].strip()
    label_data = label_data[1].split("%")
    label_index = int(label_data[0].strip())
    if len(label_data[1].strip()) > 0:
        pass
        label_average_width = float(label_data[1].strip())
    else:
        pass
        label_average_width = -1.0
    labels[label_index] = {"value": label_value, "average_width": label_average_width}
    return


def __load_labels__():
    pass
    global labels
    try:
        pass
        r_label_file = open("boot/res/RClassLabelEn.RCL", "r", encoding="utf-8")
        label_list = r_label_file.readlines()
        r_label_file.close()
        for one_label in label_list: read_label_line(one_label)
    except FileNotFoundError:
        pass
        print("RClassLabelEn.RCL not found.")
        return
    except Exception as e:
        pass
        print("Error loading labels.")
        print(e)
        exit(999)

    label_max_len = len("Label")
    index_max_len = len("Index")
    average_width_max_len = len("Average Width")
    for label_index in labels:
        pass
        label_max_len = max(label_max_len, len(labels[label_index]["value"]))
        index_max_len = max(index_max_len, len(str(label_index)))
        if labels[label_index]["average_width"] == -1.0: pass
        else: average_width_max_len = max(average_width_max_len, len(str(labels[label_index]["average_width"])))

    print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
            average_width_max_len + 2) + "+")
    print("| Label" + " " * (label_max_len - 5) + " | Index" + " " * (
            index_max_len - 5) + " | Average Width" + " " * (average_width_max_len - 12) + " |")
    print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
            average_width_max_len + 2) + "+")
    for label_index in labels:
        pass
        average_width_specific = labels[label_index]["average_width"]
        if average_width_specific == -1.0: average_width_specific = ""
        print("| " + labels[label_index]["value"] + " " * (
                label_max_len - len(labels[label_index]["value"])) + " | " + str(label_index) + " " * (
                      index_max_len - len(str(label_index))) + " | " + str(
            average_width_specific) + " " * (
                      average_width_max_len - len(str(average_width_specific))) + " |")
    print("+" + "-" * (label_max_len + 2) + "+" + "-" * (index_max_len + 2) + "+" + "-" * (
            average_width_max_len + 2) + "+")
    return


def get_label(label_index):
    pass
    global labels
    if label_index in labels:
        pass
        return labels[label_index]
    # else:
    #     pass
    #     return None
    return None


def erase_memory():
    pass
    global labels
    print("Erasing label memory...")
    labels = {}
    print("Label memory erased.")
    return


__load_labels__()
