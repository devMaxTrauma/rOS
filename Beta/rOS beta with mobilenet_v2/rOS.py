import cv2 as cv
import tensorflow as tf
import tensorflow_hub as hub

import rOSconfig

# print version of rOS
print("rOS Beta with mobilenet_v2")

# print version of imports
print("cv2 version: " + cv.__version__)
print("tf version: " + tf.__version__)
print("tf_hub version: " + hub.__version__)

# load model
print("Preparing model...")
modelURL = "https://kaggle.com/models/google/mobilenet-v2/frameworks/TensorFlow1/variations/openimages-v4-ssd-mobilenet-v2/versions/1"
print("Model Name: mobilenet_v2")
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

# load colors
print("Loading colors...")
# color file format is "name = "#RRGGBB""
colorFile = open("rOSClassColor.txt", "r")
classColors = [[], []]
for line in colorFile:
	# split line by "="
	color = line.split("=")
	# add color to list
	classColors[0].append(color[0].strip())
	classColors[1].append(color[1].strip())
	if rOSconfig.modelDebugLog:
		print("name: ", color[0].strip(), " color: ", color[1].strip())
print("Colors loaded.")

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
	# inputs: a tree-channel image of variable size - the model does not support batching. the input tensor is a tf.float32 tensor with shape [1, height, width, 3]. with values in 0.0, 1.0.
	detectorInput = tf.image.convert_image_dtype(frame, tf.float32)[tf.newaxis, ...]
	detectorOutput = model(detectorInput, as_dict=True)
	# outputs:
	# detection_boxes: a tf.float32 tensor of shape [n,4] containing bounding box coordinates in the following order: [ymin, xmin, ymax, xmax].
	# detection_scores: a tf.float32 tensor of shape [n] containing detection scores.
	# detection_class_entities: a tf.string tensor of shape [n] containing detection class entities.
	# detection_class_names: a tf.string tensor of shape [n] containing detection class names.
	# detection_class_labels: a tf.int64 tensor of shape [n] containing detection class labels.

	outputFrame = frame.copy()

	detectedObjectsCount = detectorOutput["detection_boxes"].shape[0]

	# draw boxes
	for i in range(detectedObjectsCount):
		# get box
		box = detectorOutput["detection_boxes"][i].numpy()
		# get class label
		classLabel = classLabels[detectorOutput["detection_class_labels"][i].numpy()]
		# get class color
		classColor = classColors[1][classLabels.index(classLabel)]
		# get class score
		classScore = detectorOutput["detection_scores"][i].numpy()
		# draw box
		cv.rectangle(outputFrame, (int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])), (int(box[3] * frame.shape[1]), int(box[2] * frame.shape[0])), (int(classColor[1:3], 16), int(classColor[3:5], 16), int(classColor[5:7], 16)), 2)
		# draw label
		cv.putText(outputFrame, classLabel + " " + str(classScore), (int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)


	# show frame
	if rOSconfig.rOSIsOnMac:
		cv.namedWindow("rOSBeta", cv.WINDOW_NORMAL)
		cv.imshow("rOSBeta", outputFrame)

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
