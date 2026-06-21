import cv2
import os
import numpy as np


class FaceUnlock:

    MODEL = "auth/user_face.yml"

    def __init__(self):

        self.camera = cv2.VideoCapture(0)

        self.detector = (
            cv2.CascadeClassifier(
                cv2.data.haarcascades
                +
                "haarcascade_frontalface_default.xml"
            )
        )

        self.recognizer = (
            cv2.face.LBPHFaceRecognizer_create()
        )

    # ==========================
    # GET FACE
    # ==========================

    def capture_face(self):

        while True:

            ok, frame = (
                self.camera.read()
            )

            if not ok:
                continue

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = (
                self.detector.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(120, 120)
                )
            )

            for (
                x,
                y,
                w,
                h
            ) in faces:

                face = gray[
                    y:y+h,
                    x:x+w
                ]

                face = cv2.resize(
                    face,
                    (200, 200)
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                cv2.imshow(
                    "JARVIS Unlock",
                    frame
                )

                cv2.waitKey(300)

                return face

            cv2.imshow(
                "JARVIS Unlock",
                frame
            )

            if (
                cv2.waitKey(1)
                ==
                ord("q")
            ):
                return None

    # ==========================
    # REGISTER
    # ==========================

    def register(self):

        print(
            "\nREGISTER YOUR FACE\n"
        )

        faces = []

        while len(faces) < 20:

            face = (
                self.capture_face()
            )

            if face is not None:

                faces.append(
                    face
                )

                print(
                    f"{len(faces)}/20"
                )

        labels = np.zeros(
            len(faces),
            dtype=np.int32
        )

        self.recognizer.train(
            faces,
            labels
        )

        self.recognizer.write(
            self.MODEL
        )

        return True

    # ==========================
    # VERIFY
    # ==========================

    def verify(self):

        self.recognizer.read(
            self.MODEL
        )

        face = (
            self.capture_face()
        )

        if face is None:
            return False

        label, confidence = (
            self.recognizer.predict(
                face
            )
        )

        print(
            f"Confidence: {confidence}"
        )

        return (
            label == 0
            and confidence < 50     
        )

    # ==========================
    # MAIN
    # ==========================

    def authenticate(self):

        try:

            if not os.path.exists(
                self.MODEL
            ):

                result = (
                    self.register()
                )

            else:

                print(
                    "\nVERIFY FACE\n"
                )

                result = (
                    self.verify()
                )

            return result

        finally:

            self.camera.release()

            cv2.destroyAllWindows()