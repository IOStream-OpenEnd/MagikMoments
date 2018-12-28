import unittest
import cv2
from classifier import *

class Tests(unittest.TestCase):

    def test_create_frames(self):
        vid = cv2.VideoCapture("sample_video.mp4")
        self.assertEqual(create_frames(vid), 10)

    def test_detect_face(self):
        img = cv2.imread("index.jpeg")
        #self.assertEqual(detect_face(img), "")
        pass

    def test_check_emotion():
        pass

    def test_show_face():
        pass

    def test_output():
        pass
