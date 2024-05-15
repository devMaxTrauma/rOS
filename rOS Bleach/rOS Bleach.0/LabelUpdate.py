label_file = open("rClassLabelEnDiscard.rCL", "r")
label_origin_lines = label_file.readlines()
label_file.close()

print("to 1.1")

label_file = open("rClassLabelEn.rCL", "w")
for label_origin_line in label_origin_lines:
	label_name = label_origin_line.split("=")[0].strip()
	label_index = label_origin_line.split("=")[1].strip()
	label_file.write(label_name + " = " + label_index + " % " + "\n")
label_file.close()
