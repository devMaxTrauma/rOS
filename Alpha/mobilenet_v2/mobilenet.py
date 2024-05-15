import os

import matplotlib.pyplot as plt
import tensorflow as tf

# assert float(tf.__version__[:3]) >= 2.3

_URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
zip_file = tf.keras.utils.get_file(origin=_URL, fname="flower_photos.tgz", extract=True)
flowers_dir = os.path.join(os.path.dirname(zip_file), 'flower_photos')

IMAGE_SIZE = 224
BATCH_SIZE = 64

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
	rescale=1. / 255,
	validation_split=0.2
)

train_generator = datagen.flow_from_directory(
	flowers_dir,
	target_size=(IMAGE_SIZE, IMAGE_SIZE),
	batch_size=BATCH_SIZE,
	subset='training'
)

val_generator = datagen.flow_from_directory(
	flowers_dir,
	target_size=(IMAGE_SIZE, IMAGE_SIZE),
	batch_size=BATCH_SIZE,
	subset='validation'
)

image_batch, label_batch = next(train_generator)
image_batch.shape, label_batch.shape

print(train_generator.class_indices)

labels = '\n'.join(sorted(train_generator.class_indices.keys()))
with open('flower_labels.txt', 'w') as f:
	f.write(labels)

IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
											   include_top=False,
											   weights='imagenet')
base_model.trainable = False

model = tf.keras.Sequential([
	base_model,
	tf.keras.layers.Conv2D(32, 3, activation='relu'),
	tf.keras.layers.Dropout(0.2),
	tf.keras.layers.GlobalAveragePooling2D(),
	tf.keras.layers.Dense(5, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
			  loss='categorical_crossentropy',
			  metrics=['accuracy'])

model.summary()

print("Number of trainable weights = {}".format(len(model.trainable_weights)))

history = model.fit(train_generator,
					steps_per_epoch=len(train_generator),
					epochs=5,
					validation_data=val_generator,
					validation_steps=len(val_generator))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()), 1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0, 1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

print("Number of layers in the base model: ", len(base_model.layers))

base_model.trainable = True
fine_tune_at = 100

for layer in base_model.layers[:fine_tune_at]:
	layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
			  loss='categorical_crossentropy',
			  metrics=['accuracy'])

model.summary()

