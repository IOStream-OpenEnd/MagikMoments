import cv2
import time

def create_frames(video_file, store=None):
	'''
	Our generator function that yields/saves frames of the video
	according to the store parameter
	'''

	vidcap = cv2.VideoCapture(video_file)
	success, image = vidcap.read() # returns boolean and image
	count = 0
	while success:
	  if not store: yield image 
	  else: cv2.imwrite("frames/f-%d.jpg" % count, image)     # save frame as JPG file  inside frames folder  
	  print(type(image))  
	  success,image = vidcap.read()
	  print('Read a new frame: ', success)
	  count += 1

for i in create_frames('abc.mp4', store=None):
	pass
