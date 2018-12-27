import time

import numpy as np
import cv2


class MyClassifier:

	def __init__(self):
		pass


	def create_frames(self, video_file):
		"""Generator function that yields frames of the video

		Arguments : 
		video_file = Input video file name
		"""
		
		global frame_no

		vidcap = cv2.VideoCapture(video_file)
		success, image = vidcap.read()
		while success:
			yield image
			success,image = vidcap.read()
			print(f'Read frame {frame_no}:', success)
			frame_no += 1


	def detect_face(self, img):
		"""Generator function that yields faces from frame
		
		Arguments :
		img = The numpy object with picture as a set of matices
		"""

		global face_detector1
		global face_detector2
		global face_detector3
		global face_detector4

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert img to GrayScale
		#faces = face_cascade.detectMultiScale(gray, 1.3, 5) #detect in gray
		
		faces1 = face_detector1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
		faces2 = face_detector2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
		faces3 = face_detector3.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
		faces4 = face_detector4.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        #Checking which Cascade detected a face and output only that image which detected a face.
		if len(faces1) > 0:
			detected_faces = faces1
		elif len(faces2) > 0:
			detected_faces = faces2
		elif len(faces3) > 0:
			detected_faces = faces3
		elif len(faces4) > 0:
			detected_faces = faces4
		else:
			detected_faces = None

		if detected_faces is not None: 
			for (x, y, w, h) in detected_faces:
				img = cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
				yield img[y:y+h, x:x+h] #crop color image to face & yield


	def check_smile(self, img):
		"""Check for smile inside face image

		Arguments :
		img = The numpy object with picture as a set of matices
		"""

		global frame_array

		smile = smile_detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
		for (x, y, w, h) in smile: 
		#If any smile image then resize & return along with frame_no
			try:
				img = cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
				img = cv2.resize(img, (350, 350)) # resize each image to 350x350
				frame_array.append((img,  frame_no))
				print(frame_array)
				return True
			except Exception as e:
				print(e)
				return False


	def show_face(self, img):
		"""Displays the image.

		Arguments :
		img = The numpy object with picture as a set of matices
		"""

		cv2.imshow('Image', img)
		cv2.waitKey(2) # Display for 2 secs only


	def output(self, file_name, fps, size=None):
		"""Combines the frames into video.

		Arguments :
		file_name = Output video file name
		fps = Frames per second
		size = Size of final video
		"""

		global frame_array

		if size is None:
			img = cv2.imread(frame_array[0][0])
			height, width, layers = img.shape
			size = (width,height)

		# Creating video writer object which will combine frames to create video
		out = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

		# Pass smile images from frame_array to video writer object
		for i in range(len(frame_array)):
			out.write(frame_array[i][0]) # frame_array[i][0] because we are adding the image part only. not frame_count

		out.release() # save/release output file


	def destroy(self):
		cv2.destroyAllWindows()


frame_no = 0 # Used for time stamping audio later
frame_array = [] # Array containing all smiley frames
detected_faces = None # temporary faces holder

face_detector1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_detector2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
face_detector3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
face_detector4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

classifier = MyClassifier()

for frame in classifier.create_frames("big11mbvid.mp4"): # Get frame
	for face in classifier.detect_face(frame): # Check for a face
		classifier.show_face(face)

classifier.output("MagikMoments_video.mp4", 25.0, (350,350))


classifier.destroy()


