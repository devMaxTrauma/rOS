import rKernel

rKernel.Kernel()
video = None
if rKernel.get_key("ros_running_device").value == "macbook pro":
	if rKernel.get_key("ros_camera_device").value == "macbook pro":
		video = rKernel.cv.VideoCapture(0)
	elif rKernel.get_key("ros_camera_device").value == "iphone":
		video = rKernel.cv.VideoCapture(1)
	else:
		rKernel.make_error_message("Camera device not recognized.", level="Key Error")
elif rKernel.get_key("ros_running_device").value == "raspberry pi":
	video = rKernel.cv.VideoCapture(0)
else:
	rKernel.make_error_message("Running device not recognized.", level="Key Error")

window_width = 0
window_height = 0
window_x_position = 0
window_y_position = 0

if rKernel.get_key("ros_display_device").value == "macbook pro":
	window_width = rKernel.get_key("macbook_pro_display_resolution_width_limit").value
	window_height = rKernel.get_key("macbook_pro_display_resolution_height_limit").value
	window_x_position = 0
	window_y_position = 0
elif rKernel.get_key("ros_display_device").value == "lg_full_hd":
	window_width = rKernel.get_key("lg_full_hd_display_resolution_width_limit").value
	window_height = rKernel.get_key("lg_full_hd_display_resolution_height_limit").value
	window_x_position = 0
	window_y_position = 0
else:
	rKernel.make_error_message("Display device not recognized.", level="Key Error")

rKernel.cv.namedWindow("rOS", rKernel.cv.WINDOW_NORMAL)
rKernel.cv.resizeWindow("rOS", window_width, window_height)
rKernel.cv.moveWindow("rOS", window_x_position, window_y_position)

if not video.isOpened():
	print("Fatal Error: Could not open video stream")
	exit(1)
while True:
	frameSuccess, frame = video.read()
	processing_frame = None
	if not frameSuccess:
		print("Fatal Error: Could not read frame")
		break

	if rKernel.get_key("ros_camera_device").value == "macbook pro":
		frame = rKernel.cv.resize(frame, (rKernel.get_key("macbook_pro_camera_resolution_width_limit").value,
										  rKernel.get_key("macbook_pro_camera_resolution_height_limit").value))
		processing_frame = frame.copy()
	elif rKernel.get_key("ros_camera_device").value == "iphone":
		frame = rKernel.cv.resize(frame, (rKernel.get_key("iphone_12_mini_camera_resolution_width_limit").value,
										  rKernel.get_key("iphone_12_mini_camera_resolution_height_limit").value))
		processing_frame = frame.copy()
	else:
		rKernel.make_error_message("Camera device not recognized.", level="Key Error")

	if rKernel.get_key("ros_tensorflow_enabled").value:
		input_frame = rKernel.tf.convert_to_tensor(frame, dtype=rKernel.tf.uint8)[rKernel.tf.newaxis, ...]
		output = rKernel.model(input_frame)

		if rKernel.get_key("ros_model_debug_log_enabled").value:
			print("num_detections: ", output["num_detections"])
			print("detection_classes: ", output["detection_classes"])
			print("detection_boxes: ", output["detection_boxes"])
			print("detection_scores: ", output["detection_scores"])
			print("raw_detection_boxes: ", output["raw_detection_boxes"])
			print("raw_detection_scores: ", output["raw_detection_scores"])
			print("detection_multiclass_scores: ", output["detection_multiclass_scores"])
			print("detection_anchor_indices: ", output["detection_anchor_indices"])

		detected_object_count = int(output["num_detections"].numpy())
		for detected_object in range(detected_object_count):
			if output["detection_scores"][0, detected_object] > rKernel.get_key(
					"ros_model_minimum_probability").value:
				class_id = int(output["detection_classes"][0, detected_object].numpy())
				class_name = rKernel.get_label(class_id).label
				class_color = rKernel.get_label(class_id).color
				class_average_width = rKernel.get_label(class_id).average_width
				class_distance = -1
				blue = int(class_color.blue)
				green = int(class_color.green)
				red = int(class_color.red)
				box = output["detection_boxes"][0, detected_object].numpy()

				if rKernel.get_key("ros_opencv_fill_rectangle_detected_object_mode").value == "line":
					processing_frame = rKernel.cv.rectangle(processing_frame,
															(
																int(box[1] * frame.shape[1]),
																int(box[0] * frame.shape[0])),
															(
																int(box[3] * frame.shape[1]),
																int(box[2] * frame.shape[0])),
															(blue, green, red),
															2)
					red = 255 - red
					green = 255 - green
					blue = 255 - blue

					processing_frame = rKernel.cv.putText(processing_frame, class_name,
														  (int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])),
														  rKernel.cv.FONT_HERSHEY_SIMPLEX,
														  rKernel.get_key("ros_opencv_label_font_size").value, (
															  blue, green, red),
														  rKernel.get_key("ros_opencv_label_font_thickness").value)
				elif rKernel.get_key("ros_opencv_fill_rectangle_detected_object_mode").value == "fill":
					# draw rectangle
					processing_frame = rKernel.cv.rectangle(processing_frame,
															(
																int(box[1] * frame.shape[1]),
																int(box[0] * frame.shape[0])),
															(
																int(box[3] * frame.shape[1]),
																int(box[2] * frame.shape[0])),
															(blue, green, red),
															-1)
					red = 255 - red
					green = 255 - green
					blue = 255 - blue
					# draw line
					processing_frame = rKernel.cv.rectangle(processing_frame,
															(
																int(box[1] * frame.shape[1]),
																int(box[0] * frame.shape[0])),
															(
																int(box[3] * frame.shape[1]),
																int(box[2] * frame.shape[0])),
															(blue, green, red),
															rKernel.get_key(
																"ros_opencv_line_width_detected_object").value)

					# draw text on center of box
					text_width, text_height = rKernel.cv.getTextSize(class_name, rKernel.cv.FONT_HERSHEY_SIMPLEX,
																	 rKernel.get_key(
																		 "ros_opencv_label_font_size").value,
																	 rKernel.get_key(
																		 "ros_opencv_label_font_thickness").value)[0]
					text_x = int((box[1] * frame.shape[1] + box[3] * frame.shape[1]) / 2 - text_width / 2)
					text_y = int((box[0] * frame.shape[0] + box[2] * frame.shape[0]) / 2 + text_height / 2)
					processing_frame = rKernel.cv.putText(processing_frame, class_name, (text_x, text_y),
														  rKernel.cv.FONT_HERSHEY_SIMPLEX,
														  rKernel.get_key("ros_opencv_label_font_size").value, (
															  blue, green, red),
														  rKernel.get_key("ros_opencv_label_font_thickness").value)

					if rKernel.get_key("ros_distance_calculating_enabled").value:
						box_width = int((box[3] - box[1]) * frame.shape[1])
						distance_calculate_constant = rKernel.get_key("ros_distance_calculation_constant").value
						if rKernel.get_key("ros_require_distance_calibrate").value:
							pass
						if rKernel.get_key("ros_distance_display_enabled").value and class_average_width != -1.0:
							if rKernel.get_key("ros_distance_unit").value == "meter":
								distance = class_average_width/(box_width / (
										rKernel.get_key("ros_distance_calculation_constant").value * 2))
								class_distance = distance
								if class_distance >= 1:
									class_distance_output = str(round(class_distance, 2)) + "m"
								elif class_distance < 1:
									class_distance_output = str(round(class_distance * 100, 2)) + "cm"
								processing_frame = rKernel.cv.putText(processing_frame, class_distance_output,
																	  (text_x, text_y + text_height),
																	  rKernel.cv.FONT_HERSHEY_SIMPLEX,
																	  rKernel.get_key("ros_opencv_label_font_size").value, (
																	  blue, green, red),
																	  rKernel.get_key("ros_opencv_label_font_thickness").value)

	rKernel.cv.imshow("rOS", processing_frame)

	if rKernel.cv.waitKey(1) & 0xFF == rKernel.get_key("ros_shutdown_key").value:
		break

print("rOS is closing...")
rKernel.shutdown()
video.release()
rKernel.cv.destroyAllWindows()
print("rOS closed.")
exit(0)
