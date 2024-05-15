import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from PIL import ImageOps
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

moduleHandle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"

model = hub.load(moduleHandle)

model.signatures.keys()

detector = model.signatures['default']


def downloadAndResizeImage(url, newWidth=256, newHeight=256):
	_, filename = tempfile.mkstemp(suffix=".jpg")
	response = urlopen(url)
	imageData = response.read()
	imageData = BytesIO(imageData)
	pilImage = Image.open(imageData)
	pilImage = ImageOps.fit(pilImage, (newWidth, newHeight))
	pillImageRGB = pilImage.convert("RGB")
	pillImageRGB.save(filename, format="JPEG", quality=90)
	print("Image downloaded to %s." % filename)
	return filename


imageURL = "https://upload.wikimedia.org/wikipedia/commons/f/fb/20130807_dublin014.JPG"
downloadedImagePath = downloadAndResizeImage(imageURL, 3872, 2592)


def loadImg(path):
	img = tf.io.read_file(path)
	img = tf.image.decode_jpeg(img, channels=3)
	return img


def run_detector(detector, path):
	img = loadImg(path)

	converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
	result = detector(converted_img)

	result = {key: value.numpy() for key, value in result.items()}
	print("Found %d objects." % len(result["detection_scores"]))

	print(result["detection_boxes"])
	print(result["detection_class_entities"])
	print(result["detection_scores"])


run_detector(detector, downloadedImagePath)
