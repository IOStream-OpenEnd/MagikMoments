import unittest
import os

import cv2
from moviepy.editor import VideoFileClip

from src.Test1 import classifier, trim_merge


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
        print("Enter the number of faces in index.jpeg")
        no_of_faces = int(input())
        # to count no. of faces in the frame
        count = 0

        face_d1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        face_d2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        face_d3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        face_d4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

        # counting no. of frames
        for face in classifier.MyClassifier.detect_face(cv2.imread("index.jpeg"), face_d1, face_d2, face_d3, face_d4):
            if face[0] is not None:
                count += 1
                classifier.MyClassifier.show_face(face[0])

        # if no. of faces(as given by user) is equal to the number of faces detected by detect_face than test pass
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
        pass

    def test_show_face(self):
        img = cv2.imread("index.jpeg")
        self.assertEqual(classifier.MyClassifier.show_face(img), None)


if __name__ == '__main__':
    unittest.main()
