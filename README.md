# MagikMoments

Finds the "magic" and the most happy moments of a given movie and makes a trailer out of it
few changes

# Installation procedure

TBD

# Running the code

TBD

# Action Plan for Complete Project

To complete the project we need to do the following task one by one.

- [x] Find a Python Module that can take video file (.mp4 or something) and convert it into frames. (OpenCV)

- [x] implement that module into our code. (Creating frames)

- [x] Save the frames into an array. (We can use a generator function and directly work on the images. It is also CPU/memory efficient)

- [ ] Check which frames are magic moments using images processing and machine learning.

- [x] Convert those frames into a video. (Merging frames)

## Action Plan for Machine Learning Part

- [ ] We need dataset to feed the Machine Learning algorithm.

- [x] We will use OpenCV's HAAR filters and cascades for facial detection.

- [x] Then we need to minimize the noise from the images. To do this, we will need to crop the image and convert it to grayscale.

- [ ] If one image have 2 faces, we will need to resolve that problem.

- [ ] Next We will need an algorithm to classify that facial image according to emotion.

- [ ] We will use array index to compare frames with images and get only those frames which are classified as happy.

- [x] The control will switch back to merging the frames. (If merging dynamically, then that can also be done. Currently, we assume that we are combining stored images)
