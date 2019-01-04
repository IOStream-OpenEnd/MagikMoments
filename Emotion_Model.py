"""

Mounting google drive to colab

"""

from google.colab import drive
drive.mount('/content/drive')

"""
Checking GPU usage
"""
!ln -sf /opt/bin/nvidia-smi /usr/bin/nvidia-smi
!pip install gputil
!pip install psutil
!pip install humanize
import psutil
import humanize
import os
import GPUtil as GPU
GPUs = GPU.getGPUs()
# XXX: only one GPU on Colab and isn’t guaranteed
gpu = GPUs[0]
def printm():
  process = psutil.Process(os.getpid())
  print("Gen RAM Free: " + humanize.naturalsize( psutil.virtual_memory().available ), " | Proc size: " + humanize.naturalsize( process.memory_info().rss))
  print("GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB".format(gpu.memoryFree, gpu.memoryUsed, gpu.memoryUtil*100, gpu.memoryTotal))

printm()

cd '/content/drive/My Drive'



import numpy as np
import os
import time
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.layers import Dense, Flatten
from keras.layers import Input
from keras.models import Model
from keras.utils import np_utils
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

"""
Loading images from the data set

"""
path = '/content/drive/My Drive/weird_Data21'
folders = os.listdir(path)
img_data_list = []
img_names = []

for _ in folders:
    img_list = os.listdir(path+'/' + _)
    for img in img_list:
        img_path = path + '/' + _ + '/' + img
        img_names.append(img_path)
    print(f"image - {len(img_names)}")
print(f"Final length of img_names - {len(img_names)}")

happy = img_names[0:1500]
not_happy = img_names[5000: 6501]

"""
Loading images and converting to required size

"""
start_ti = time.time()
for img1, img2 in zip(happy, not_happy):
    lp_ti = time.time()
    imgee1 = image.load_img(img1, target_size=(224, 224))
    imgee2 = image.load_img(img2, target_size=(224, 224))
    x1 = image.img_to_array(imgee1)
    x2 = image.img_to_array(imgee2)
    x1 = np.expand_dims(x1, axis=0)
    x2 = np.expand_dims(x2, axis=0)
    x1 = preprocess_input(x1)
    x2 = preprocess_input(x2)
    img_data_list.insert(0, x1)
    img_data_list.insert(len(img_data_list), x2)
    print(f"count - {len(img_data_list)}")
    print(f"time taken for {len(img_data_list)} = {time.time() - lp_ti}")
  
print(f"Total time = {time.time() - start_ti}")

img_data = np.array(img_data_list)

print(img_data.shape)
img_data = np.rollaxis(img_data, 1, 0)
print(img_data.shape)
img_data = img_data[0]
print(img_data.shape)


num_classes = 2
num_of_samples = img_data.shape[0]
labels = np.ones((num_of_samples,), dtype='int64')
labels[0:1500] = 0
labels[1500:] = 1
names = ['happy', 'not happy']

"""
Converting to one hot encoding

"""

Y = np_utils.to_categorical(labels, num_classes)

x, y = shuffle(img_data, Y, random_state=2)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

"""

Loading and customizing the VGG-16 Model

"""

image_input = Input(shape=(224, 224, 3))
model = VGG16(input_tensor=image_input, include_top=True, weights='imagenet')
model.summary()
last_layer = model.get_layer('block5_pool').output
x = Flatten(name='flatten')(last_layer)
x = Dense(128, activation='relu', name='fc1')(x)
x = Dense(128, activation='relu', name='fc2')(x)
out = Dense(num_classes, activation='softmax', name='output')(x)
Magik = Model(image_input, out)
Magik.summary()

"""

Freezing the appropriate layers

"""
for layer in Magik.layers[:-3]:
    layer.trainable = False
Magik.summary()
Magik.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

"""
Training the model on the training set and testing on the validation set

"""

t = time.time()
hist = Magik.fit(X_train, y_train, batch_size=32, epochs=50, verbose=1, validation_data=(X_test, y_test))
print('Training time: %s' % (t - time.time()))
(loss, accuracy) = Magik.evaluate(X_test, y_test, batch_size=10, verbose=1)

print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))

"""
Saving the trained model and weights

"""

Magik.save("Magik2.h5")
Magik.save_weights("MagikWeights2.h5")
