# The program uses a tensorflow backend along with Keras and Scikit Learn
# The strategy used is transfer learning.
# The model used is a pretrained VGG-16 (a pretrained 16 layer convolutional neural net)
# The term verbose at certain places is just to show the training in an animated fasion

import os
import time

import numpy as np

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.layers import Dense, Activation, Flatten
from keras.layers import merge, Input
from keras.models import Model
from keras.utils import np_utils

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split


cur_dir = os.getcwd()
path = cur_dir + '/emotion'
folders = os.listdir(path)

img_data_list=[]

for _ in folders:
	img_list = os.listdir(path+'/' + _)
	for img in img_list:
		img_path = path + '/' + _ + '/' + img
		img = image.load_img(img_path, target_size=(224, 224))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		x = preprocess_input(x)
		img_data_list.append(x)


img_data = np.array(img_data_list)

print(img_data.shape)

img_data = np.rollaxis(img_data, 1, 0)
print(img_data.shape)
img_data = img_data[0]
print(img_data.shape)

num_classes = 4
num_of_samples = img_data.shape[0]
labels = np.ones((num_of_samples,), dtype='int64')

labels[0:202] = 0
labels[202:404] = 1
labels[404:606] = 2
labels[606:] = 3


names = ['angry', 'happy', 'neutral', 'sad']


Y = np_utils.to_categorical(labels, num_classes)

x, y = shuffle(img_data,Y, random_state=2)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

image_input = Input(shape=(224, 224, 3))

model = VGG16(input_tensor=image_input, include_top=True, weights='imagenet')

model.summary()

last_layer = model.get_layer('fc2').output

out = Dense(num_classes, activation='softmax', name='output')(last_layer)
MagikModel = Model(image_input, out)
MagikModel.summary()


for layer in MagikModel.layers[:-1]:
	layer.trainable = False


MagikModel.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

MagikModel.summary()


t = time.time()
train = MagikModel.fit(X_train, y_train, batch_size=32, epochs=50, verbose=1, validation_data=(X_test, y_test))


(loss, accuracy) = MagikModel.evaluate(X_test, y_test, batch_size=10, verbose=1)

