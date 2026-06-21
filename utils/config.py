from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    USER_NAME = os.getenv("USER_NAME", "Boss")

    WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()

    VOICE_RATE = int(
        os.getenv("VOICE_RATE", "175")
    )

    VOICE_VOLUME = float(
        os.getenv("VOICE_VOLUME", "1.0")
    )

    FACE_TOLERANCE = float(
        os.getenv("FACE_TOLERANCE", "0.50")
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    DEFAULT_CITY = os.getenv(
        "DEFAULT_CITY",
        "Forbesganj"
    )