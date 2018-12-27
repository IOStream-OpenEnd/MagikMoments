# MagikMoments

Finds the "magic" and the most happy moments of a given movie and makes a trailer out of it.


## Requirements :

Need a working Python 3.6 environment along with pip installed. 

To install the external modules, open cmd/terminal and navigate inside the MagikMoments directory.
Then run :
* On windows :
    ```bash
    pip install -r requirements.txt
    ```

* On Linux :
    ```bash
    pip3 install -r requiremnts.txt 
    ```
## Running the code :

Open CMD/Terminal, navigate inside MagikMoments/src/Test1/ directory and run :
* On Windows :
    ```bash
    python classifier.py
    ``` 
* On Linux :
    ```bash
    python3 classifier.py
    ```

## Working (Internal):

1. Specify the video file to be used.
2. The video file will be sent to `create_frames` method which is a generator function yielding frames.
3. The frame from `create_frames` will be passed to `detect_face` method which will check for faces and display if any found.
4. All the face images will be stored in the global array - `frame_array` which will be for creating the final output by combining all the frames. 
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
