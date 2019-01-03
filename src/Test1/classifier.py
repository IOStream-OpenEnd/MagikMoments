import os.path

import cv2

from src.Test1.trim_merge import CombineClips
from keras.models import load_model
model=load_model("Magik2.h5")
model.load_weights("MagikWeights2.h5")

class MyClassifier:

    def __init__(self):
        pass

    @staticmethod
    def create_frames(video_file):
        """Generator function that yields frames of the video.

        :param video_file: Input video file name.
        :returns :  If file not exists -> None.
                    If reads frame -> yields frames as numpy.ndarray objects.
                    If reads no frame -> None.
        """

        frame_no = 0  # Used for time stamping audio

        if not os.path.isfile(video_file):  # check if file exists
            return None

        vidcap = cv2.VideoCapture(video_file)
        success, image = vidcap.read()
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # Get fps of video
        while success:

            # 5*fps = 5 seconds. So if frame_no is a multiple of (5*fps), then we get every first frame of the 1st,5th,10th,15th second and so on
            if frame_no is 0 or frame_no % (5 * fps) == 0:
                print(f'Read frame : {frame_no} ({int(frame_no / fps)}th second) ')
                yield (image, frame_no, fps)

            success, image = vidcap.read()

            if not success:
                return None

            frame_no += 1

    @staticmethod
    def detect_face(img, face_d1, face_d2, face_d3, face_d4):
        """Generator function that yields detected faces from the frame.

        :param img: The numpy.ndarray object with picture as a set of matrices.
        :param face_d1: Obj loaded with haarcascade_frontalface_default.xml
        :param face_d2: Obj loaded with haarcascade_frontalface_alt2.xml
        :param face_d3: Obj loaded with haarcascade_frontalface_alt.xml
        :param face_d4: Obj loaded with haarcascade_frontalface_alt_tree.xml
        :returns : If face detected -> (img, 1)
                   If no face detected -> (None, 0)
        """

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert img to GrayScale
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5) #detect in gray

        faces1 = face_d1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces2 = face_d2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces3 = face_d3.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces4 = face_d4.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        # Check which Cascade detected face(s)
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
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                yield tuple([img, 1])  # Sending complete image for testing purpose # Issue of haarcascade false positives
                # yield (img[y:y + h, x:x + h], 1)  # Crop color image to face & yield

        else:
            return tuple([None, 0])

    @staticmethod
    def check_emotion(img):

        # Code and docstring will be added accordingly
        pass

    @staticmethod
    def show_face(img):
        """Displays the image.

        :param img: The numpy.ndarray object with picture as a set of matrices
        :return : None
        """

        cv2.imshow('Image', img)
        cv2.waitKey(250)  # Display for 0.25 secs only
        return None

    @staticmethod
    def destroy():
        """Destroys all OpenCV created windows.

        :return: None
        """
        cv2.destroyAllWindows()
        return None


def main():
    """Checks for faces in frames.

    :return: None
    """

    moments_timestamps = []

    input_video = "sample_video.mp4"

    # face detectors
    face_d1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_d2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    face_d3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_d4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

    classifier = MyClassifier()
    trim_merge = CombineClips()

    for frame, frame_no, fps in classifier.create_frames(input_video):  # Get frame, frame_no, fps

        count = 0  # To count no. of faces in the frame

        for face, boolean in classifier.detect_face(frame, face_d1, face_d2, face_d3, face_d4):  # Check for a face

            if face is not None:
                if MyClassifier.check_emotion(face):
                    count += 1
                classifier.show_face(face)

                if count is 1:  # Append once even if two faces inside the frame
                    moments_timestamps.append(frame_no / fps)

        print(f"Face count = {count}")
        print()

    trim_merge.cut_moments(input_video, moments_timestamps)
    trim_merge.combine_clips("some_file.mp4")

    classifier.destroy()
    return None


if __name__ == '__main__':

    main()
