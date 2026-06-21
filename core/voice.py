import threading
import queue
import time

import speech_recognition as sr
import pyttsx3
import pythoncom

from utils.config import Config


class VoiceEngine:

    def __init__(self):

        # ======================
        # CONVERSATION MODE
        # ======================

        self.conversation_mode = False
        self.last_interaction = 0
        self.timeout = 2000

        # ======================
        # SPEECH RECOGNITION
        # ======================

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        # ======================
        # STATE
        # ======================

        self.running = False
        self.speaking = False

        self.speech_queue = queue.Queue()

        # ======================
        # START TTS
        # ======================

        self.tts_thread = threading.Thread(
            target=self._tts_worker,
            daemon=True
        )

        self.tts_thread.start()

        print("[VOICE READY]")

    # ======================
    # SPEAK
    # ======================

    def speak(
        self,
        text
    ):

        if not text:
            return

        print(
            f"[TTS QUEUED] {text}"
        )

        self.speech_queue.put(
            str(text)
        )

    # ======================
    # TTS ENGINE
    # ======================

    def _tts_worker(self):

        pythoncom.CoInitialize()

        engine = pyttsx3.init(
            driverName="sapi5"
        )

        engine.setProperty(
            "rate",
            Config.VOICE_RATE
        )

        engine.setProperty(
            "volume",
            Config.VOICE_VOLUME
        )

        try:

            voices = (
                engine.getProperty(
                    "voices"
                )
            )

            for voice in voices:

                if (
                    "david"
                    in voice.name.lower()
                ):

                    engine.setProperty(
                        "voice",
                        voice.id
                    )

                    break

        except:
            pass

        while True:

            text = (
                self.speech_queue.get()
            )

            if text is None:
                break

            self.speaking = True

            try:

                print(
                    f"[TTS SPEAKING] {text}"
                )

                engine.say(
                    text
                )

                engine.runAndWait()

                print(
                    "[TTS DONE]"
                )

            except Exception as e:

                print(
                    f"TTS ERROR: {e}"
                )

            self.speaking = False

            self.speech_queue.task_done()

        engine.stop()

        pythoncom.CoUninitialize()

    # ======================
    # LISTEN
    # ======================

    def listen_once(self):

        try:

            with sr.Microphone() as source:

                print(
                    "[LISTENING]"
                )

                audio = (

                    self.recognizer.listen(

                        source,

                        timeout=8,

                        phrase_time_limit=10

                    )

                )

            text = (

                self.recognizer
                .recognize_google(
                    audio
                )

                .lower()

            )

            print(
                f"[HEARD] {text}"
            )

            return text

        except sr.WaitTimeoutError:

            return None

        except sr.UnknownValueError:

            return None

        except Exception as e:

            print(
                f"MIC ERROR: {e}"
            )

            return None

    # ======================
    # WAKE WORD
    # ======================

    def contains_wake_word(
        self,
        text
    ):

        if not text:
            return False

        current = time.time()

        # continue conversation

        if self.conversation_mode:

            if (

                current
                -
                self.last_interaction

                <

                self.timeout

            ):

                self.last_interaction = current

                return True

            else:

                self.conversation_mode = False

        # activate

        if (

            Config.WAKE_WORD

            in

            text.lower()

        ):

            self.conversation_mode = True

            self.last_interaction = current

            return True

        return False

    # ======================
    # COMMAND EXTRACTION
    # ======================

    def extract_command(
        self,
        text
    ):

        return (

            text

            .lower()

            .replace(
                Config.WAKE_WORD,
                ""
            )

            .strip()

        )

    # ======================
    # LOOP
    # ======================

    def start_listening(
        self,
        callback
    ):

        self.running = True

        def loop():

            while self.running:

                if self.speaking:

                    time.sleep(
                        0.3
                    )

                    continue

                text = (
                    self.listen_once()
                )

                if text:

                    callback(
                        text
                    )

        threading.Thread(

            target=loop,

            daemon=True

        ).start()

    # ======================
    # STOP
    # ======================

    def stop(self):

        self.running = False

        self.speech_queue.put(
            None
        )