import cv2 as cv

video = cv.VideoCapture(0)

escapeKey = '\x1b'
shotKey = ' '

while True:
	frameSuccess, frame = video.read()

	if not frameSuccess:
		print('Can\'t receive frame (stream end?). Exiting ...')
		break

	cv.namedWindow('rOS', cv.WINDOW_NORMAL)
	cv.imshow('Capture', frame)

	if cv.waitKey(1) == ord(escapeKey):
		break
	elif cv.waitKey(1) == ord(shotKey):
		cv.imwrite('devPics/Done.jpg', frame)
		break

video.release()
cv.destroyAllWindows()
