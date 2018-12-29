import os.path

import cv2

from src.Test1.trim_merge import CombineClips

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

        global frame_no
        global fps

        if not os.path.isfile(video_file):  # check if file exists
            return None

        vidcap = cv2.VideoCapture(video_file)
        success, image = vidcap.read()
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))  #  Get fps of video
        while success:

            # 5*fps = 5 seconds. So if frame_no is a multiple of (5*fps), then we get every first frame of the 1st,5th,10th,15th second and so on
            if frame_no is 0 or frame_no % (5 * fps) == 0:
                print(f'Read frame : {frame_no} ({int(frame_no / fps)}th second) ')
                yield image

            success, image = vidcap.read()

            if not success: return None

            frame_no += 1

    @staticmethod
    def detect_face(img):
        """Generator function that yields detected faces from the frame.

        :param img: The numpy.ndarray object with picture as a set of matrices.
        :returns : If face detected -> (img, 1)
                   If no face detected -> (None, 0)
        """

        global face_detector1
        global face_detector2
        global face_detector3
        global face_detector4

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert img to GrayScale
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5) #detect in gray

        faces1 = face_detector1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces2 = face_detector2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces3 = face_detector3.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces4 = face_detector4.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

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
                yield (img, 1) # Sending complete image for testing purpose # Issue of haarcascade false positives
                # yield (img[y:y + h, x:x + h], 1)  # Crop color image to face & yield

        else:
            return tuple((None, 0))

    @staticmethod
    def check_emotion():

        # Code and docstring will be added accordingly

        pass

    @staticmethod
    def show_face(img):
        """Displays the image.

        :param img: The numpy.ndarray object with picture as a set of matrices
        :return : None
        """

        cv2.imshow('Image', img)
        cv2.waitKey(2000)  # Display for 2 secs only
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

    global frame_no
    global fps
    global moments_timestamps

    input_video = "sample_video.mp4"

    classifier = MyClassifier()
    trim_merge = CombineClips(input_video)

    for frame in classifier.create_frames(input_video):  # Get frame

        count = 0  # To count no. of faces in the frame

        for face in classifier.detect_face(frame):  # Check for a face

            if face[0] is not None:

                count += 1
                classifier.show_face(face[0])

                if count is 1:  # Append once even if two faces inside the frame
                    moments_timestamps.append(frame_no / fps)

        print(f"Face count = {count}")
        print()

    trim_merge.cut_moments(moments_timestamps)
    trim_merge.combine_clips("some_file.mp4")

    classifier.destroy()
    return None


if __name__ == '__main__':

    fps = 0
    frame_no = 0  # Can be used for time stamping audio later
    moments_timestamps = []

    face_detector1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_detector2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    face_detector3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_detector4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

    main()
