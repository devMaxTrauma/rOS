import cv2
import numpy as np

# OpenCV의 사전 학습된 모델 경로 설정
prototxt_path = "path/to/model.prototxt"
caffemodel_path = "path/to/model.caffemodel"

# 클래스 레이블 설정
class_labels = ["background", "class1", "class2", "class3"]  # 예시 클래스명

# 모델 불러오기
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# 카메라 열기
cap = cv2.VideoCapture(0)  # 0은 기본 카메라를 의미합니다. 필요에 따라 카메라 인덱스를 수정해야 할 수 있습니다.

while True:
	# 카메라 프레임 읽기
	ret, frame = cap.read()

	# 이미지 전처리 및 입력 데이터 생성
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

	# 네트워크를 통한 사물인식 수행
	net.setInput(blob)
	detections = net.forward()

	# 감지 결과를 반복하여 사물인식 정보 추출
	for i in range(detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.5:  # 임계값 설정
			class_id = int(detections[0, 0, i, 1])
			class_label = class_labels[class_id]
			box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
			(startX, startY, endX, endY) = box.astype("int")

			# 사물인식 결과를 프레임에 표시
			cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, class_label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	# 프레임 출력
	cv2.imshow("Object Detection", frame)

	# 'q' 키를 누르면 종료
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
