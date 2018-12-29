import os

from moviepy.editor import VideoFileClip, concatenate_videoclips


class CombineClips:
	def __init__(self, input_file):
		"""Stores the parameters as class attributes for cu_moments() to access.

		:param input_file:  Name of input file.

		"""

		self.moments_timestamp = None
		self.input_file = input_file
		self.duration = VideoFileClip(input_file).duration  # Total seconds of the video

	def cut_moments(self, moments_timestamp):
		"""Cuts the input video at the time stamps, each of 5 seconds - 2.5 seconds before and 2.5 seconds after time stamp.

		:param moments_timestamp: List/Tuple containing the time stamps.
		:return: None
		"""

		self.moments_timestamp = moments_timestamp
		clip_count = 0

		if not os.path.exists("clips"):  # Check for clips directory
			os.mkdir("clips")  # Create it if not existing to store clips

		with VideoFileClip(self.input_file) as video:
			for stamp in self.moments_timestamp:
				if stamp <= 2.5:
					new_clip = video.subclip(0, stamp + 2.5)  # Because; 1.We can't take 2.5 before 0th second, 2.Even if stamp is 2.5 it is going to be (2.5 -2.5) which is 0th second.
				elif (stamp + 2.5) > self.duration:
					new_clip = video.subclip(stamp - 2.5, self.duration)  # Because we can't take end > actual duration of video
				else:
					new_clip = video.subclip(stamp - 2.5, stamp + 2.5)  # In the normal case
				new_clip.write_videofile(f"clips/clip-{clip_count}.mp4")  # , audio_codec='aac')
				clip_count += 1

		return None

	@staticmethod
	def combine_clips(output_file_name):
		"""Searches inside the clips directory and merges clips in ascending order.

		:param output_file_name: Name of output file.
		:return: None
		"""

		video_files = [] # will store video_clips

		# making name list of all mp4 files with filename starting with "test"
		video_names=[("clips/" + n) for n in os.listdir('clips/') if n[:4]=="clip" and n[-4:]=='.mp4']

		# sorting of list according to index which follows "clip-" and precedes ".mp4" in file name
		video_names.sort(key=lambda name: int(name.split("-")[1].split(".")[0]))

		for clip_name in video_names:
			clip = VideoFileClip(clip_name)  # Load clip
			video_files.append(clip)  # Append to video_files

		final_clip = concatenate_videoclips(video_files) # Merge all clips
		final_clip.write_videofile(output_file_name)  # Output merged clips

		return None
