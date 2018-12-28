import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import os

class CombineClips:
	def __init__(self,key_moments_timestamp_array=None,last_frame_timestamp=None):

		# constructor need to receive timestamps for the required frames as well as
		# the timestamp of last frame of original video for cut_moments method
		self.key_moments_timestamp_array=key_moments_timestamp_array
		self.last_frame_timestamp=last_frame_timestamp

	def cut_moments(self):
		for stamp in range(len(self.key_moments_timestamp_array)):
			# extracting subclips and saving as 'test{INDEX}.mp4'
			ffmpeg_extract_subclip("sample_video.mp4", max(0,self.key_moments_timestamp_array[stamp]-2) , min(self.key_moments_timestamp_array[stamp]+2,self.last_frame_timestamp) , targetname="test{}.mp4".format((stamp)+1))

	def combine_clips(self):
		#this function drops audio currently
		video_index=0

		# making list of all mp4 files with filename starting with "test"
		videofiles=[n for n in os.listdir('.') if n[0:4]=="test" and n[-4:]=='.mp4']

		# sorting of list according to index which follows "test" in file name
		videofiles = sorted(videofiles, key=lambda item: int( item.partition('.')[0][4:]))

		# capturing first clip
		cap=cv2.VideoCapture(videofiles[0])

		# creating video writer object in which all clips will be combined.
		# this writer object initialization uses fps and size values from cap(first clip)
		out=cv2.VideoWriter("final.mp4", cv2.VideoWriter_fourcc(*'mp4v'),cap.get(cv2.CAP_PROP_FPS),(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

		while(cap.isOpened()):
			ret, frame = cap.read()

			# when current clip ends
			if frame is None:	
				print("end of video " + str(video_index) + " .. starting next one")
				video_index += 1

				# when all clips have finished appending
				if video_index >= len(videofiles):
					break
				cap = cv2.VideoCapture(videofiles[video_index])
				ret, frame = cap.read()

			# displaying frame
			cv2.imshow('frame',frame)

			# writing frame to write object
			out.write(frame)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# wrapping up
		cap.release()
		out.release()
		print("end.")

timestamp=[x for x in range(1,1000,5)]
cc=CombineClips(timestamp,120)
cc.cut_moments()
cc.combine_clips()