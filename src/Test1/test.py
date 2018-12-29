import unittest

import cv2

from src.Test1 import classifier


class Tests(unittest.TestCase):

    def test_create_frames(self):
        vid = cv2.VideoCapture("xyz.mp4")
        self.assertEqual(classifier.MyClassifier.create_frames(vid), None)

    def test_detect_face(self):
        img = cv2.imread("index.jpeg")
        self.assertEqual(classifier.MyClassifier.detect_face(img), (None, 0))
        pass

    def test_check_emotion(self):
        pass

    def test_show_face(self):
        img = cv2.imread("index.jpeg")
        self.assertEqual(classifier.MyClassifier.show_face(img), None)

    def test_destroy(self):
        self.assertEqual(classifier.MyClassifier.destroy(), None)

    # The outputs need to checked. That I don't know how to.