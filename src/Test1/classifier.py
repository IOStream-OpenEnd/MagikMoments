import os.path

from keras.models import load_model
from keras.preprocessing import image as im
import cv2
import numpy as np

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
    def detect_face(img, face_d1, face_d2, face_d3):
        """Generator function that yields detected faces from the frame.

        :param img: The numpy.ndarray object with picture as a set of matrices.
        :param face_d1: Obj loaded with haarcascade_frontalface_default.xml
        :param face_d2: Obj loaded with haarcascade_frontalface_alt.xml
        :param face_d3: Obj loaded with haarcascade_frontalface_alt2.xml
        :returns : If face detected -> (img, 1)
                   If no face detected -> (None, 0)
        """

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert img to GrayScale

        faces1 = face_d1.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces2 = face_d2.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        faces3 = face_d3.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        # Check which Cascade detected face(s)
        if len(faces1) > 0:
            detected_faces = faces1
        elif len(faces2) > 0:
            detected_faces = faces2
        elif len(faces3) > 0:
            detected_faces = faces3
        else:
            detected_faces = None

        if detected_faces is not None:

            # x,y = x,y coordinates
            # w,h = width, height
            for (x, y, w, h) in detected_faces:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # yield tuple([img, 1])  # Sending complete image for testing purpose # Issue of haarcascade false positives
                yield (img, x, y, w, h)  # Crop color image to face & yield

        else:
            return None

    @staticmethod
    def check_emotion(img, x, y, w, h, model, emotions):
        """Checks if image is happy / not happy.

        :param img: The numpy.ndarray object with picture as a set of matrices.
        :param x: x-coordinate of the face in img
        :param y: y-coordinate of face in img
        :param w: width of face
        :param h: height of face
        :param model: pre trained model with weights
        :param emotions: list of possible classifications
        :return: predicted label
        """

        adjust_img = img[y:y+h, x:x+w]  # Crop img to the face
        adjust_img = cv2.resize(adjust_img, (224, 224))  # Resize img to fit the ML model

        img_tensor = im.img_to_array(adjust_img)
        img_tensor = np.expand_dims(img_tensor, axis=0)

        img_tensor /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

        predictions = model.predict(img_tensor)  # store probabilities of 2 facial expressions

        label = emotions[np.argmax(predictions)]  # Get label with most probability
        confidence = np.max(predictions)  # Get the confidence of that label

        cv2.putText(img, label + " : " + str(confidence), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return label

    @staticmethod
    def show_face(img, emotion):
        """Displays the image.

        :param img: The numpy.ndarray object with picture as a set of matrices
        :param emotion: The emotion label
        :return : None
        """

        cv2.imshow(emotion, img)
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

    input_video = input("Enter path to the video file : ")

    # Load face detector objects
    face_d1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_d2 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_d3 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    # Load ML model and compile
    model = load_model("Magik2.h5")

    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

    emotions = ('happy', 'not happy')

    classifier = MyClassifier()
    trim_merge = CombineClips()

    for frame, frame_no, fps in classifier.create_frames(input_video):  # Get frame, frame_no, fps

        count = 0  # To count no. of faces in the frame

        for face, x, y, w, h in classifier.detect_face(frame, face_d1, face_d2, face_d3):  # Check for a face

            emotion = classifier.check_emotion(face, x, y, w, h, model, emotions)
            if emotion is "happy":
                count += 1
                classifier.show_face(face, emotion)

                if count is 1:  # Append timestamp once even if two faces inside the frame
                    moments_timestamps.append(frame_no / fps)

        print(f"Face count = {count}")
        print()

    trim_merge.cut_moments(input_video, moments_timestamps)
    trim_merge.combine_clips("some_file.mp4")

    classifier.destroy()
    return None


if __name__ == '__main__':

    main()
