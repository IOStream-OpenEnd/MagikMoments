# **MagikMoments**

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

## Running The Test

TBD

## Working (Internal):

1. Specify the video file to be used.
2. The video file will be sent to `create_frames` method which is a generator function yielding frames.
3. The frame from `create_frames` will be passed to `detect_face` method which will check for faces and display if any found.
4. The faces from `detect_face` will be passed to `check_emotion` method which will check if the face is happy or not and that will also be 
   stored.
5. All the face images will be stored in the global array - `frame_array` which will be for creating the final output by combining all the 
   frames. 
6. The method `cut_moments` will be called, where it will be check which moments are happy. 4-sec clips will be cut for each moments and it will
   be stored into a array.
7. That array will be passed to `combine_clips` where they will be combined.

## Contribution 

Please read contribution.md for details on our code of conduct, and the process for submitting pull requests to us.

## Author

Supragya Raj

List of Contributors
- Kogam22
- masterchef2209
- aayush1205
- DeboDevelop
- shawayux

## License

TBD
