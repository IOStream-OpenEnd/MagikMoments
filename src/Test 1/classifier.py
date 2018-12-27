import time

import numpy as np
import cv2


class MyClassifier:
	def __init__(self):
		pass

	def create_frames(self, video_file):
		'''Generator function that yields frames of the video'''
		
		vidcap = cv2.VideoCapture(video_file)
		success, image = vidcap.read()
		count = 0
		while success:
			yield image
			success,image = vidcap.read()
			print(f'Read frame {count}:', success)
			count += 1

	def detect_face(self, img, face_cascade):
		'''Another Generator function that yields faces from the frame'''
		
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5) #detect in gray
		for (x,y,w,h) in faces:
		    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		    yield img[y:y+h, x:x+h] #crop color image to face & yield


	def show_face(self, img):
		cv2.imshow('Image', img)
		cv2.waitKey(2)

	def destroy(self):
		cv2.destroyAllWindows()


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = MyClassifier()

for frame in classifier.create_frames("big3.mp4"):
	for face in classifier.detect_face(frame, face_cascade):
		classifier.show_face(face)




