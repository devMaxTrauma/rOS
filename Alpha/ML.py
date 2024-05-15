import cv2 as cv
import numpy as np
from tensorflow.keras import layers, models


def create_model():
	print('Creating model...')
	model = models.Sequential([
		layers.Conv2D(32, (3, 3), activation='relu', input_shape=(1080, 1920, 3)),
		layers.MaxPooling2D((2, 2)),
		layers.Conv2D(64, (3, 3), activation='relu'),
		layers.MaxPooling2D((2, 2)),
		layers.Conv2D(64, (3, 3), activation='relu'),
		layers.Flatten(),
		layers.Dense(64, activation='relu'),
		layers.Dense(1, activation='softmax')
	])
	print("Model created.")

	model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

	print("Model compiled.")
	return model


def preprocess_image(image_path):
	# 이미지 로드
	image = cv.imread(image_path)
	# Check if the image was loaded correctly
	if image is None:
		print("Failed to load image at {image_path}")
		return None
	# 이미지 크기 조정 등의 전처리 수행
	processed_image = cv.resize(image, (1920, 1080))
	processed_image = processed_image.astype('float32') / 255.0  # 이미지 정규화
	return processed_image


# 데이터 로드 및 전처리
train_data = []
labels = []

for i in range(1, 101, 1):
	# 이미지 로드
	processed_img = preprocess_image('devPics/image' + str(i) + '.jpg')
	# 이미지를 train_data에 추가
	if processed_img is not None:
		train_data.append(processed_img)
		# 라벨 추가
		labels.append(0 if "Gio" else 1)
		print("Image {i} loaded and processed.")
	else:
		print("Image {i} failed to load and process.")

test_data = cv.imread('devPics/Done.jpg')

# 모델 생성
model = create_model()

print('a')

# 모델 학습
model.fit(x=np.array(train_data), y=np.array(labels), epochs=2)

# 모델 저장
model.save('model.h5')

print('b')

# 모델 평가
video = cv.VideoCapture(0)
# escapeKey as esc
escapeKey = '\x1b'

while True:
	frameSuccess, frame = video.read()

	if not frameSuccess:
		print('Can\'t receive frame (stream end?). Exiting ...')
		break

	cv.namedWindow('rOS', cv.WINDOW_NORMAL)
	cv.imshow('Video', frame)

	# 모델 평가
	processed_frame = cv.resize(frame, (1920, 1080))
	processed_frame = processed_frame.astype('float32') / 255.0  # 이미지 정규화

	processed_frame = np.expand_dims(processed_frame, axis=0)
	predictions = model.predict(processed_frame)

	if cv.waitKey(1) == ord(escapeKey):
		break
