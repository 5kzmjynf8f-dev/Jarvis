import sys

from PyQt6.QtWidgets import QApplication

from auth.pin_unlock import PinUnlock
from ui.main_window import MainWindow

from core.brain import JarvisBrain
from core.voice import VoiceEngine
from auth.face_unlock import FaceUnlock


class Jarvis:

    def __init__(self):

        self.app = QApplication(
            sys.argv
        )

        # ======================
        # FACE UNLOCK
        # ======================

        unlock = FaceUnlock()

        if not unlock.authenticate():

            print(
                "FACE UNLOCK FAILED. SWITCHING TO PASSWORD AUTHENTICATION."
            )

            pin = PinUnlock()

            if not pin.authenticate():

                print(
                    "PASSWORD AUTHENTICATION FAILED SELF DESTRUCTION INITIATED."
                )

                sys.exit()

        # ======================
        # LOAD CORE
        # ======================

        self.window = MainWindow()

        self.brain = JarvisBrain()

        self.voice = VoiceEngine()

        # ======================
        # START VOICE
        # ======================

        self.voice.start_listening(
            self.handle_voice
        )

        self.window.show()

        self.voice.speak(
            "Systems online. Welcome Boss."
        )

        self.window.add_log(
            "JARVIS ONLINE"
        )

    # ======================
    # VOICE
    # ======================

    def handle_voice(
        self,
        text
    ):

        self.window.add_log(
            f"You: {text}"
        )

        if (
            not self.voice
            .contains_wake_word(
                text
            )
        ):
            return

        command = (

            self.voice
            .extract_command(
                text
            )

        )

        if not command:

            return

        try:

            response = (

                self.brain
                .process(
                    command
                )

            )

        except Exception as e:

            response = (
                f"Error: {e}"
            )

        self.window.add_log(

            f"JARVIS: {response}"

        )

        self.voice.speak(
            response
        )

    # ======================
    # RUN
    # ======================

    def run(self):

        code = (
            self.app.exec()
        )

        self.voice.stop()

        sys.exit(
            code
        )


if __name__ == "__main__":

    Jarvis().run()