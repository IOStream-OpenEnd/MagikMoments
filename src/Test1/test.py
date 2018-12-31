import unittest
import os
import cv2
import classifier,trim_merge
from moviepy.editor import VideoFileClip

class Tests(unittest.TestCase):

	def test_create_frames(self):
		# fetch video
		vid=cv2.VideoCapture("sample_video.mp4")

		# getting fps
		fps = int(vid.get(cv2.CAP_PROP_FPS))

		# in create_frames we get frame after every 5 secs so number of frames returned should be equal to (total number of frames in video)/(number of frames per 5 seconds) + 1 {for frame_no=0}
		self.assertEqual(len(list(classifier.MyClassifier.create_frames("sample_video.mp4"))),int(vid.get(cv2.CAP_PROP_FRAME_COUNT)/(5*fps))+1)

	def test_cut_moments(self):
		# CombineClips object
		tm=trim_merge.CombineClips()

		# fetching the video clip
		clip=VideoFileClip("sample_video.mp4")

		# building timestamps list with each timestamp atleast 5 seconds away from the other one
		timestamps=[x for x in range(0,int(clip.duration),5)]

		# calling cut_moments
		tm.cut_moments(timestamps,"sample_video.mp4")

		# if clips folder exists, the number of timestamps should be equal to number of subclips generated
		if os.path.exists("clips"):
			clip_list=os.listdir("clips")
			self.assertEqual(len(clip_list),len(timestamps))
		else:
			print("clips folder does not exist")
			self.assertEqual(1,-1)
    	
    	
    # def test_detect_face(self):
    #     img = cv2.imread("index.jpeg")
    #     self.assertEqual(len(list(classifier.MyClassifier.detect_face(img))), 1)

    # def test_check_emotion(self):
    #     pass

    # def test_show_face(self):
    #     img = cv2.imread("index.jpeg")
    #     self.assertEqual(classifier.MyClassifier.show_face(img), None)

    
    	

if __name__=='__main__':
	unittest.main()