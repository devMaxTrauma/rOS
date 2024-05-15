import cv2 as cv
import tensorflow as tf
import tensorflow_hub as hub

import rOSconfig

# print version of imports
print("cv2 version: " + cv.__version__)
print("tf version: " + tf.__version__)
print("tf_hub version: " + hub.__version__)

# load model
print("Preparing model...")
modelURL = "https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1/frameworks/TensorFlow2/variations/fpn-640x640/versions/1"
print("Model Name: SSD MobileNet V1")
print("Model URL: " + modelURL)
print("Loading model...")
model = hub.load(modelURL)
print("Model loaded.")

# load labels
print("Loading labels...")
# label file format is "name = id"
labelFile = open("rOSClassLabel.txt", "r")
classLabels = []
for line in labelFile:
	# split line by "="
	label = line.split("=")
	# add label to list
	classLabels.append(label[0].strip())
print("Labels loaded.")

# open camera
video = cv.VideoCapture(0)

if not video.isOpened():
	print("Could not open video")
	exit(1)

while True:
	# read frame
	frameSuccess, frame = video.read()
	if not frameSuccess:
		print("Could not read frame")
		break

	# process frame
	# todo late
	# tensorfy frame tf.uint8 tensor with shape [1, height, width, 3] with values in [0, 255]
	detectorInput = tf.convert_to_tensor(frame, dtype=tf.uint8)[tf.newaxis, ...]
	detectorOutput = model(detectorInput)
	# output has bellow things:
	# num_detections: a tf.int tensor with only one value, the number of detections
	# detection_boxes: a tf.float32 tensor of shape [N, 4] containing the coordinates of the detection boxes. coordinates are in normalized form and are given in the order [ymin, xmin, ymax, xmax]
	# detection_classes: a tf.int tensor of shape [1, 100] containing the class for each detection
	# detection_scores: a tf.float32 tensor of shape [1, 100] containing the score for each detection
	# detection_multiclass_scores: a tf.float32 tensor of shape [1, 100, 90] containing the class scores for each detection
	# raw_detection_boxes: a tf.float32 tensor of shape [1, 1917, 4] containing the detection boxes
	# raw_detection_scores: a tf.float32 tensor of shape [1, 1917, 91] containing the detection scores
	# detection_anchor_indices: a tf.int tensor of shape [1, 100] containing the anchor indices of the detections

	# show frame
	if rOSconfig.rOSIsOnMac:
		cv.namedWindow("rOS", cv.WINDOW_FULLSCREEN)
		# show detector output with boxes
		processedFrame = frame.copy()
		if rOSconfig.modelDebugLog:
			print("num_detections: ", detectorOutput["num_detections"])
			print("detection_classes: ", detectorOutput["detection_classes"])
			print("detection_scores: ", detectorOutput["detection_scores"])

		detectedObjectCount = int(detectorOutput["num_detections"].numpy())

		for detectedObject in range(detectedObjectCount):
			if detectorOutput["detection_scores"][0, detectedObject] > rOSconfig.modelMinProbability:
				# get box
				box = detectorOutput["detection_boxes"][0, detectedObject].numpy()
				# get class
				classId = int(detectorOutput["detection_classes"][0, detectedObject].numpy())
				# get score
				score = float(detectorOutput["detection_scores"][0, detectedObject].numpy())
				# get label
				label = classLabels[classId - 1]
				# draw box
				processedFrame = cv.rectangle(processedFrame,
											  (int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])),
											  (int(box[3] * frame.shape[1]), int(box[2] * frame.shape[0])), (0, 255, 0),
											  2)
				# draw label
				processedFrame = cv.putText(processedFrame, label,
											(int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])),
											cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		cv.imshow("rOS", processedFrame)
	# todo late

	else:
		cv.namedWindow("rOS", cv.WINDOW_FULLSCREEN)
		cv.imshow("rOS", frame)

	# exit
	if cv.waitKey(1) & 0xFF == ord(rOSconfig.exitKey):
		print("rOS is closing...")
		break

# release camera
print("Releasing camera...")
video.release()
cv.destroyAllWindows()
print("You can close this window now.")
