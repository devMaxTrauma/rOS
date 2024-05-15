class Manager:
    import os
    class Key:
        positive_signs = ["True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "t", "T", "y", "Y"]
        negative_signs = ["False", "false", "0", "no", "No", "NO", "off", "Off", "OFF", "f", "F", "n", "N"]
        def __init__(self, key_data):
            self.name = key_data.split("<name>")[1].split("</>")[0].strip()
            self.type = key_data.split("<type>")[1].split("</>")[0].strip()
            self.value = key_data.split("<value>")[1].split("</>")[0].strip()
            self.comment = key_data.split("<comment>")[1].split("</>")[0].strip()
            if self.type == "bool":
                if self.value in self.positive_signs:
                    self.value = True
                elif self.value in self.negative_signs:
                    self.value = False
                else:
                    self.value = None
            elif self.type == "int":
                try:
                    self.value = int(self.value)
                except ValueError:
                    self.value = None
            elif self.type == "float":
                try:
                    self.value = float(self.value)
                except ValueError:
                    self.value = None
            elif self.type == "str":
                self.value = str(self.value)

            self.type = type(self.value)

    def __init__(self):
        self.key_root = self.os.path.dirname(__file__)

    def add_key(self, name, type, value, comment):
        try:
            key_file = open(self.key_root+"/RKey.RKY", encoding="utf-8", mode="r")
            key_lines = key_file.readlines()
            key_file.close()
        except FileNotFoundError:
            key_lines = []
        try:
            key_file = open(self.key_root+"/RKey.RKY", encoding="utf-8", mode="w")
            for line in key_lines:
                key_file.write(line)
            key_file.write(
                "<name> " + name + " </> " + "<type> " + type + " </> " + "<value> " + value + " </> " + "<comment> " + comment + " </>\n")
            key_file.close()
        except FileNotFoundError:
            self._make_error("Failed to write to RKey.RKY")

    def get_key(self, name):
        try:
            key_file = open(self.key_root+"/RKey.RKY", encoding="utf-8", mode="r")
            key_lines = key_file.readlines()
            key_file.close()
        except FileNotFoundError:
            self._make_error("RKey.RKY not found")

        key_names = []
        key_types = []
        key_values = []
        key_comments = []
        keys = []

        for line in key_lines:
            keys.append(self.Key(line))
            if line.__contains__("<name>"):
                key_names.append(line.split("<name>")[1].split("</>")[0].strip())
            if line.__contains__("<type>"):
                key_types.append(line.split("<type>")[1].split("</>")[0].strip())
            if line.__contains__("<value>"):
                key_values.append(line.split("<value>")[1].split("</>")[0].strip())
            if line.__contains__("<comment>"):
                key_comments.append(line.split("<comment>")[1].split("</>")[0].strip())

        expected_key_name = self.string_suggestion(name, key_names)
        if expected_key_name is None:
            return None

        key_index = key_names.index(expected_key_name)

        return keys[key_index]

    def string_suggestion(self, search, candidates):
        for i in range(len(candidates)):
            candidates[i] = candidates[i].lower()
        search = search.lower()
        possibility = [0].copy() * len(candidates)
        for i in range(len(candidates)):
            for j in range(len(search)):
                if len(candidates[i]) <= j:
                    break
                if search[j] == candidates[i][j]:
                    possibility[i] += 2
                elif candidates[i].__contains__(search[j]):
                    possibility[i] += 1

        max_possibility = 0
        max_possibility_count = 0

        for i in range(len(possibility)):
            if possibility[i] > max_possibility:
                max_possibility = possibility[i]
                max_possibility_count = 1
            elif possibility[i] == max_possibility:
                max_possibility_count += 1

        if max_possibility_count > 1:
            return None
        else:
            max_possibility_index = possibility.index(max_possibility)

        return candidates[max_possibility_index]

    def _make_error(self, error):
        print("Error: " + error)
        exit(1)
