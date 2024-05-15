import cv2 as cv
import tensorflow as tf
import tensorflow_hub as hub

assert float(tf.__version__[:3]) >= 2.3

model = tf.keras.Sequential([
	hub.KerasLayer(
		"https://www.kaggle.com/models/google/mobilenet-v2/frameworks/TensorFlow2/variations/035-128-classification/versions/2")
])
model.build([None, 128, 128, 3])
model.summary()

print("Model loaded.")

video = cv.VideoCapture(0)
exitKey = '\x1b'

while True:
	frameSuccess, frame = video.read()

	if not frameSuccess:
		print('Can\'t receive frame (stream end?). Exiting ...')
		break

	cv.namedWindow('rOS', cv.WINDOW_NORMAL)

	# 이미지 크기 조정
	processed_image = cv.resize(frame, (128, 128))
	processed_image = processed_image.astype('float32') / 255.0  # 이미지 정규화

	processed_image = tf.expand_dims(processed_image, axis=0)

	# 모델 추론
	processed_frame = model(processed_image)
	class_names = processed_frame['detection_class_names']

	# 화면에 출력
	cv.putText(frame, class_names, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
	cv.imshow('rOS', frame)

	if cv.waitKey(1) == ord(exitKey):
		break
