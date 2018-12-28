# MagikMoments

Finds the "magic" and the most happy moments of a given movie and makes a trailer out of it.


## Requirements :

Need a working Python 3.6 environment along with pip installed. 

To install the external modules, open CMD/Terminal and navigate inside the MagikMoments directory.
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

# Action Plan for Complete Project (Revised) :

To complete the project we need to do the following task one by one.

- [x] Create frames of given video.

- [x] Detect faces from the frames. Should be able to detect multiple faces in one image.

- [ ] Detect hyper emotion from the faces.

- [ ] Use timestamps or array or something to store the exact time/frame for the trim.

- [ ] For each hyper emotion(more like so much emotion), from the original video create a mini video containing 2 secs before the emotion and 2 secs after.

- [ ] Include audio in those mini videos. Either don't remove it during the trim or add it appropriately as per the original later. 

- [ ] Combine all the mini videos into a single.

- [ ] Perform Test Driven Development (TDD) using any testing framework.

- [ ] Create documentation for the project.