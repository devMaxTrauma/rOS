from rKernel import _negative_signs
from rKernel import _positive_signs


class Key:
	name = ""
	type = None
	value = None
	coment = ""

	def __init__(self, name, value, coment):
		self.name = name
		self.value = value
		self.coment = coment
		self.type = type(value)


keys = []


def load_keys():
	global keys
	keys = []
	key_file = open("rKey.rKY", "r")
	key_name_max_length = len("Name")
	key_type_max_length = len("Type")
	key_value_max_length = len("Value")
	key_comment_max_length = len("Comment")
	for line in key_file.readlines():
		key_name = line.split(":")[0].strip()
		key_type = line.split(":")[1].strip().split("=")[0].strip()
		key_value = line.split("=")[1].strip().split("<?>")[0].strip()
		comment = line.split("<?>")[1].strip()

		if key_type == "string":
			key_value = key_value[1:-1]
			key_type = str(key_value)
		elif key_type == "int":
			key_value = int(key_value)
		elif key_type == "float":
			key_value = float(key_value)
		elif key_type == "bool":
			if key_type in _positive_signs:
				key_value = True
			elif key_type in _negative_signs:
				key_value = False
		key_type = type(key_value)

		if len(key_name) > key_name_max_length:
			key_name_max_length = len(key_name)
		if len(str(key_type)) > key_type_max_length:
			key_type_max_length = len(str(key_type))
		if len(str(key_value)) > key_value_max_length:
			key_value_max_length = len(str(key_value))
		if len(str(comment)) > key_comment_max_length:
			key_comment_max_length = len(str(comment))
		keys.append(Key(key_name, key_value, comment))

	key_file.close()

	print("Name" + " " * (key_name_max_length - len("Name")) + " | " + "Type" + " " * (
			key_type_max_length - len("Type")) + " | " + "Value" + " " * (
				  key_value_max_length - len("Value")) + " | " + "Comment" + " " * (
				  key_comment_max_length - len("Comment")) + " |")
	for i in range(len(keys)):
		print(keys[i].name + " " * (key_name_max_length - len(keys[i].name)) + " | " + str(keys[i].type) + " " * (
				key_type_max_length - len(str(keys[i].type))) + " | " + str(keys[i].value) + " " * (
					  key_value_max_length - len(str(keys[i].value))) + " | " + keys[i].coment + " " * (
					  key_comment_max_length - len(keys[i].coment)) + " |")


def string_matcher(_search, candidates, wildcard_char="*", case_sensitive=False):
	possibility = [0].copy() * len(candidates)
	max_candidate_length = 0
	for i in range(len(candidates)):
		if len(candidates[i]) > max_candidate_length:
			max_candidate_length = len(candidates[i])

	for i in range(len(candidates)):
		import math
		if len(candidates[i]) < len(_search):
			possibility[i] += max_candidate_length - (len(candidates[i]) - len(_search))

	for i in range(len(candidates)):
		for j in range(len(_search)):
			if _search[j] == wildcard_char:
				possibility[i] += 1
				continue
			if len(candidates[i]) <= j:
				break
			if not case_sensitive:
				search_alphabet_lowerfy = _search[j].lower()
				candidate_alphabet_lowerfy = candidates[i][j].lower()
				if search_alphabet_lowerfy == candidate_alphabet_lowerfy:
					possibility[i] += 2
				elif candidate_alphabet_lowerfy.__contains__(search_alphabet_lowerfy):
					possibility[i] += 1
			else:
				if _search[j] == candidates[i][j]:
					possibility[i] += 4
				elif candidates[i].__contains__(_search[j]):
					possibility[i] += 2
				elif _search[j].lower() == candidates[i][j].lower():
					possibility[i] += 2
				elif candidates[i].__contains__(_search[j].lower()):
					possibility[i] += 1

	max_possibility = 0
	max_possibility_count = 0
	max_possibility_list = []

	for i in range(len(possibility)):
		if possibility[i] > max_possibility:
			max_possibility = possibility[i]
			max_possibility_count = 1
			max_possibility_list = [candidates[i]]
		elif possibility[i] == max_possibility:
			max_possibility_count += 1
			max_possibility_list.append(candidates[i])

	if max_possibility_count > 1:
		return max_possibility_list
	else:
		max_possibility_index = possibility.index(max_possibility)

	return [candidates[max_possibility_index]]


def boot():
	load_keys()


boot()

while True:
	search = input("Search: ").strip()

	search_name_enabled = False
	search_comment_enabled = False
	search_value_enabled = False
	search_type_enabled = False

	if search.startswith("exit"):
		break
	elif search.startswith("reload"):
		boot()
		continue
	elif search.startswith("name"):
		search_name_enabled = True
		search = search[5:].strip()
	elif search.startswith("comment"):
		search_comment_enabled = True
		search = search[8:].strip()
	elif search.startswith("value"):
		search_value_enabled = True
		search = search[6:].strip()
	elif search.startswith("type"):
		search_type_enabled = True
		search = search[5:].strip()
	elif search.startswith("add"):
		key_name = input("Name: ").lower()
		key_type = input("Type: ").lower()
		key_value = input("Value: ").lower()
		key_comment = input("Comment: ").lower()
		key_file = open("rKey.rKY", "a")
		key_file.write(key_name + " : " + key_type + " = " + key_value + " <?> " + key_comment + "\n")
		key_file.close()
		load_keys()
		continue
	elif search.startswith("remove"):
		key_name = input("Name: ").lower()
		key_file = open("rKey.rKY", "r")
		lines = key_file.readlines()
		key_file.close()
		key_file = open("rKey.rKY", "w")
		for line in lines:
			if not line.startswith(key_name):
				key_file.write(line)
		key_file.close()
		load_keys()
		continue
	elif search.startswith("edit"):
		target_key_name = input("Name: ").lower()
		key_file = open("rKey.rKY", "r")
		lines = key_file.readlines()
		key_file.close()
		key_file = open("rKey.rKY", "w")
		for line in lines:
			if not line.startswith(target_key_name):
				key_file.write(line)
			else:
				key_name = input("Name: ").lower()
				key_type = input("Type: ").lower()
				key_value = input("Value: ").lower()
				key_comment = input("Comment: ").lower()
				key_file.write(key_name + " : " + key_type + " = " + key_value + " <?> " + key_comment + "\n")
		key_file.close()
		continue
	else:
		search_name_enabled = True
		search_comment_enabled = True
		search_value_enabled = True
		search_type_enabled = True

	key_names = []
	key_comments = []
	key_values = []
	key_types = []
	for key in keys:
		key_names.append(key.name)
		key_comments.append(key.comment)
		key_values.append(str(key.value))
		key_types.append(str(key.type))

	name_matches = []
	comment_matches = []
	value_matches = []
	type_matches = []

	if search_name_enabled:
		name_matches = string_matcher(search, key_names)
	if search_comment_enabled:
		comment_matches = string_matcher(search, key_comments)
	if search_value_enabled:
		value_matches = string_matcher(search, key_values)
	if search_type_enabled:
		type_matches = string_matcher(search, key_types)

	matches = []
	for key in keys:
		if key.name in name_matches:
			matches.append(key)
		if key.comment in comment_matches:
			matches.append(key)
		if str(key.value) in value_matches:
			matches.append(key)
		if str(key.type) in type_matches:
			matches.append(key)

	max_name_length = len("Name")
	max_comment_length = len("Comment")
	max_value_length = len("Value")
	max_type_length = len("Type")

	for match in matches:
		if len(match.name) > max_name_length:
			max_name_length = len(match.name)
		if len(match.comment) > max_comment_length:
			max_comment_length = len(match.comment)
		if len(str(match.value)) > max_value_length:
			max_value_length = len(str(match.value))
		if len(str(match.type)) > max_type_length:
			max_type_length = len(str(match.type))

	print("results: ")
	print("-" * (max_name_length + max_comment_length + max_value_length + max_type_length + 12))
	print("Name" + " " * (max_name_length - len("Name")) + " | " + "Type" + " " * (
			max_type_length - len("Type")) + " | " + "Value" + " " * (
				  max_value_length - len("Value")) + " | " + "Comment" + " " * (
				  max_comment_length - len("Comment")) + " |")
	for match in matches:
		print(match.name + " " * (max_name_length - len(match.name)) + " | " + str(match.type) + " " * (
				max_type_length - len(str(match.type))) + " | " + str(match.value) + " " * (
					  max_value_length - len(str(match.value))) + " | " + match.comment + " " * (
					  max_comment_length - len(match.comment)) + " |")

	print("-" * (max_name_length + max_comment_length + max_value_length + max_type_length + 12))
