# MagikMoments

Finds the "magic" and the most happy moments of a given movie and makes a trailer out of it
few changes

# Requirements

To run the code The following needs to be installed.
- Python 3.x
- OpneCV
- Numpy

# Installation procedure

Follow the process to install open CV.

1. Open the terminal and install all dependencies

sudo apt-get install --assume-yes build-essential cmake git
sudo apt-get install --assume-yes pkg-config unzip ffmpeg qtbase5-dev python-dev python3-dev python-numpy python3-numpy
sudo apt-get install --assume-yes libopencv-dev libgtk-3-dev libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev
sudo apt-get install --assume-yes libavcodec-dev libavformat-dev libswscale-dev libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt-get install --assume-yes libv4l-dev libtbb-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev
sudo apt-get install --assume-yes libvorbis-dev libxvidcore-dev v4l-utils vtk6
sudo apt-get install --assume-yes liblapacke-dev libopenblas-dev libgdal-dev checkinstall

2. Download the OpenCV Source and unzip the file and change to the OpenCV folder

wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv.zip
cd opencv-3.3.0

3. Execute Make and compile with multiple processors

mkdir build
cd build/    
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D FORCE_VTK=ON -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_CUBLAS=ON -D CUDA_NVCC_FLAGS="-D_FORCE_INLINES" -D WITH_GDAL=ON -D WITH_XINE=ON -D BUILD_EXAMPLES=ON ..
make -j $(($(nproc) + 1))

4. Install OpenCV

udo make install
sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
sudo apt-get update

5. Testing your OpenCV Install using Python

$ python
>>> import cv2
>>> cv2.__version__

Credit for Installation procedure : http://carlosdeoliveira.net/en/general/install-opencv-3-3-0-for-linux-mint-18-2ubuntu-for-deep-learning/

# Running the code

TBD

# Action Plan for Complete Project

To complete the project we need to do the following task one by one.

- [x] Find a Python Module that can take video file (.mp4 or something) and convert it into frames. (OpenCV)

- [x] implement that module into our code. (Creating frames)

- [x] Save the frames into an array. (We can use a generator function and directly work on the images. It is also CPU/memory efficient)

- [x] Detect human faces from frames. (Faces are recognizable in PR 14)

- [ ] Check which faces are magic moments using images processing and machine learning.

- [x] Convert those frames into a video. (Merging frames)

## Action Plan for Machine Learning Part

- [x] We need dataset to feed the Machine Learning algorithm. (Datasets listed in one open issue)

- [x] We will use OpenCV's HAAR filters and cascades for facial detection.

- [x] Then we need to minimize the noise from the images. To do this, we will need to crop the image and convert it to grayscale.

- [x] If one image have 2 faces, we will need to resolve that problem.(Resolved)

- [ ] Next we need an algorithm to classify that facial image according to emotion.

- [ ] We will use array index to compare frames with images and get only those frames which are classified as happy. (Only happy ?)

- [x] The control will switch back to merging the frames. (If merging dynamically, then that can also be done. Currently, we assume that we are combining stored images)
