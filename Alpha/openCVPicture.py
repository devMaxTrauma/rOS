import cv2 as cv

video = cv.VideoCapture(0)
# escapeKey as esc
escapeKey = '\x1b'
imageCount = 0
folderPath = "devPics/image"

while True:
	frameSuccess, frame = video.read()

	if not frameSuccess:
		print('Can\'t receive frame (stream end?). Exiting ...')
		break

	cv.namedWindow('rOS', cv.WINDOW_NORMAL)
	cv.imshow('Video', frame)

	# save frame as jpg
	cv.imwrite(folderPath + str(imageCount) + '.jpg', frame)
	imageCount += 1

	if imageCount > 100:
		break

	if cv.waitKey(1) == ord(escapeKey):
		break

video.release()
cv.destroyAllWindows()
