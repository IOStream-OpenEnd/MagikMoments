import cv2


class MyClassifier:

    def __init__(self):
        pass

    @staticmethod
    def create_frames(video_file):
        """Generator function that yields frames of the video.

        Arguments :
        video_file = Input video file name
        """

        global frame_no

        vidcap = cv2.VideoCapture(video_file)
        success, image = vidcap.read()
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        while success:
            # 5*fps = 5 seconds. So if frame_no is a multiple of (5*fps), then we get every first frame of the 1st,5th,10th,15th second and so on
            if frame_no is 0 or frame_no % (5 * fps) == 0:
                print(f'Read frame : {frame_no} ({int(frame_no / fps)}th second) ')
                yield image  # return img (for testing purpose)

            success, image = vidcap.read()

            if not success:
                return False

            frame_no += 1

    @staticmethod
    def detect_face(img):
        """Generator function that yields detected faces from the frame.

        Arguments :
        img = The numpy object with picture as a set of matrices
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
                yield (img, 1) # Sending complete image for testing purpose
                # original line is 73
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

        Arguments :
        img = The numpy object with picture as a set of matrices
        """

        cv2.imshow('Image', img)
        cv2.waitKey(2000)  # Display for 2 secs only

    @staticmethod
    def output():

        # Code and docstring will be added accordingly

        pass

    @staticmethod
    def destroy():
        cv2.destroyAllWindows()


def main():
    classifier = MyClassifier()

    print()

    for frame in classifier.create_frames("sample_video.mp4"):  # Get frame

        count = 0  # To count no. of faces in the frame

        for face in classifier.detect_face(frame):  # Check for a face

            if face[0] is not None:
                classifier.show_face(face[0])
                count += 1

        print(f"Face count = {count}")
        print()

    # classifier.output("MagikMoments_video.mp4", 25.0, (350, 350))
    # Check why commented in line 108

    classifier.destroy()


if __name__ == '__main__':

    # frame_array = []  # Use not defined currently. Check line 108
    frame_no = 0  # Can be used for time stamping audio later

    face_detector1 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_detector2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    face_detector3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_detector4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

    main()
