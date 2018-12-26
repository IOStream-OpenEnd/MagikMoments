# MagikMoments

Finds the "magic" and the most happy moments of a given movie and makes a trailer out of it
few changes

# Installation procedure

TBD

# Running the code

TBD

# Action Plan

To complete the project we need to do the following task one by one.

- [x] Find a Python Module that can take video file (.mp4 or something) and convert it into frames. (OpenCV)

- [x] implement that module into our code. (Creating frames)

- [ ] Save the frames into an array.

- [ ] Check which frames are magic moments using images processing and machine learning.

- [x] Convert those frames into a video. (Merging frames)

#Action Plan for Machine Learning Part

- [ ] We need dataset to feed the Machine Learning algorithm.

- [ ] We need to minimize the noise from the images. To do this, we will need to crop the image and convert it to grayscale.

- [ ] If one image have 2 faces, we will need to resolve that problem.

- [ ] Then we will use OpenCV's HAAR filters and cascades for facial detection.

- [ ] Next We will need an algorithm to classify that facial image according to emotion.

- [ ] We will use array index to compare frames with images and get only those frames which are classified as happy.

- [ ] The control will switch back to merging the frames.
