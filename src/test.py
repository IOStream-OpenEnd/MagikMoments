import unittest
import os

import cv2
from moviepy.editor import VideoFileClip
from keras.models import load_model

from src import classifier, trim_merge


class Tests(unittest.TestCase):

    def test_create_frames(self):
        # fetch video
        vid = cv2.VideoCapture("sample_video.mp4")

        # getting fps
        fps = int(vid.get(cv2.CAP_PROP_FPS))

        # in create_frames we get frame after every 5 secs so number of frames returned should be equal to (total number of frames in video)/(number of frames per 5 seconds) + 1 {for frame_no=0}
        self.assertEqual(len(list(classifier.MyClassifier.create_frames("sample_video.mp4"))), int(vid.get(cv2.CAP_PROP_FRAME_COUNT) / (5 * fps)) + 1)

    def test_cut_moments(self):
        # CombineClips object
        tm = trim_merge.CombineClips()

        # fetching the video clip
        clip = VideoFileClip("sample_video.mp4")

        # building timestamps list with each timestamp at least 5 seconds away from the other one
        timestamps = [x for x in range(0, int(clip.duration), 5)]

        # calling cut_moments
        tm.cut_moments("sample_video.mp4", timestamps)

        # if clips folder exists, the number of timestamps should be equal to number of sub clips generated
        if os.path.exists("clips"):
            clip_list = os.listdir("clips")
            self.assertEqual(len(clip_list), len(timestamps))
        else:
            print("clips folder does not exist")
            self.assertEqual(1, -1)

    def test_detect_face(self):
        # get the number of faces in "index.jpeg" from the user
        img_name = input("Enter image name with path : ")

        if not os.path.exists(img_name):
            print(f"File {img_name} does not exist!")
            self.assertEqual(1, -1)

        no_of_faces = int(input(f"Enter the no. of faces in {img_name} : "))
        # to count no. of faces in the frame
        count = 0

        face_d1 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        face_d2 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        face_d3 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

        # counting no. of frames
        for face, x, y, w, h in classifier.MyClassifier.detect_face(cv2.imread("index.jpeg"), face_d1, face_d2, face_d3):
            if face is not None:
                count += 1
                classifier.MyClassifier.show_face(face, "none")

        # if no. of faces(as given by user) is equal to the number of faces detected by detect_face than test pass
        print("Haarcascades can sometimes not detect a face. Try with another image.")
        self.assertEqual(count, no_of_faces)

    def test_combine_clips(self):
        output_file_name = "some_file.mp4"

        # CombineClips object
        tm = trim_merge.CombineClips()

        # fetching the video clip
        clip = VideoFileClip("sample_video.mp4")

        # building timestamps list with each timestamp at least 5 seconds away from the other one
        timestamps = [x for x in range(0, int(clip.duration), 5)]

        # calling cut_moments
        tm.cut_moments("sample_video.mp4", timestamps)

        # if clips folder exists, the number of timestamps should be equal to number of sub clips generated
        if os.path.exists("clips"):
            clip_list = os.listdir("clips")
            self.assertEqual(len(clip_list), len(timestamps))
        trim_merge.CombineClips.combine_clips(output_file_name)
        self.assertEquals(os.path.isfile("some_file.mp4"), True)

    def test_check_emotion(self):
        # get the number of faces in "index.jpeg" from the user
        img_name = input("Enter image name with path : ")

        if not os.path.exists(img_name):
            print(f"File {img_name} does not exist!")
            self.assertEqual(1, -1)

        emotion = input("Is the person in the image happy / not happy ? : ")
        if emotion != "happy" and emotion != "not happy":
            print("Please enter proper emotion")
            self.assertEqual(1, -1)

        model = load_model("Magik2.h5")

        model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

        emotions = ('happy', 'not happy')

        face_d1 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        face_d2 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        face_d3 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

        # counting no. of frames
        for face, x, y, w, h in classifier.MyClassifier.detect_face(cv2.imread("index.jpeg"), face_d1, face_d2, face_d3):
            if face is not None:
                detected_emotion = classifier.MyClassifier.check_emotion(face, x, y, w, h, model, emotions)
                print(detected_emotion)

        self.assertEqual(emotion, detected_emotion)

    def test_show_face(self):
        pass


if __name__ == '__main__':
    unittest.main()
