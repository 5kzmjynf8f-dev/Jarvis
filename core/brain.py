import datetime
import webbrowser
import urllib.parse
import requests
import wikipedia
import pyjokes
import psutil
import pyautogui
import pywhatkit

from google import genai

from utils.config import Config
from core.controller import PCController


SYSTEM_PROMPT = f"""
You are JARVIS.

User:
{Config.USER_NAME}

Be concise.
"""


class JarvisBrain:

    def __init__(self):

        self.pc = PCController()

        self.client = None

        try:

            if Config.GEMINI_API_KEY:

                self.client = genai.Client(
                    api_key=Config.GEMINI_API_KEY
                )

        except:

            self.client = None

    # ==================
    # MAIN
    # ==================

    def process(
        self,
        command
    ):

        command = (
            command
            .lower()
            .strip()
        )

        print(
            "[COMMAND]",
            command
        )

        if not command:
            return "Say something."

        # MEDIA CONTROL

        media = self.media_control(
            command
        )

        if media:
            return media

        # PLAY

        if command.startswith(
            "play "
        ):

            return (
                self.play_media(
                    command
                )
            )

        # SEARCH

        if command.startswith(
            "search "
        ):

            return (
                self.google_search(
                    command
                )
            )

        # WEATHER

        if (
            "weather"
            in command
        ):

            return (
                self.get_weather(
                    command
                )
            )

        # OPEN

        if command.startswith(
            "open "
        ):

            return (

                self.open_site(

                    command.replace(
                        "open ",
                        ""
                    )

                )

            )

        # INFO

        if "time" in command:
            return self.get_time()

        if "date" in command:
            return self.get_date()

        if "battery" in command:
            return self.get_battery()

        if "system" in command:
            return self.get_system()

        if "joke" in command:
            return pyjokes.get_joke()

        # WIKI

        if command.startswith(
            "wiki "
        ):

            try:

                return wikipedia.summary(

                    command.replace(
                        "wiki ",
                        ""
                    ),

                    sentences=2

                )

            except:

                return (
                    "Nothing found."
                )

        # AI

        return (
            self.ask_gemini(
                command
            )
        )

    # ==================
    # PLAY
    # ==================

    def play_media(
        self,
        command
    ):

        query = (

            command

            .replace(
                "play",
                ""
            )

            .replace(
                "on youtube",
                ""
            )

            .strip()

        )

        if not query:

            return (
                "What should I play?"
            )

        try:

            pywhatkit.playonyt(
                query
            )

            return (
                f"Playing {query}"
            )

        except Exception as e:

            return (
                str(e)
            )

    # ==================
    # MEDIA
    # ==================

    def media_control(
        self,
        command
    ):

        try:

            if (
                command
                ==
                "pause"
            ):

                pyautogui.press(
                    "k"
                )

                return (
                    "Paused"
                )

            if (
                command
                ==
                "resume"
            ):

                pyautogui.press(
                    "k"
                )

                return (
                    "Resumed"
                )

            if (
                command
                ==
                "next"
            ):

                pyautogui.hotkey(
                    "shift",
                    "n"
                )

                return (
                    "Next video"
                )

        except:

            pass

        return None

    # ==================
    # SEARCH
    # ==================

    def google_search(
        self,
        command
    ):

        query = (

            command

            .replace(
                "search",
                ""
            )

            .strip()

        )

        webbrowser.open(

            "https://google.com/search?q="

            +

            urllib.parse.quote(
                query
            )

        )

        return (
            f"Searching {query}"
        )

    # ==================
    # WEATHER
    # ==================

    def get_weather(
        self,
        command
    ):

        city = (

            command

            .replace(
                "weather in",
                ""
            )

            .replace(
                "weather",
                ""
            )

            .strip()

        )

        if not city:

            city = (
                Config.DEFAULT_CITY
            )

        try:

            r = requests.get(

                f"https://wttr.in/{city}?format=3"

            )

            return (
                r.text
            )

        except:

            return (
                "Weather unavailable"
            )

    def open_site(
        self,
        site
    ):

        url = (
            "https://"
            +
            site
            +
            ".com"
        )

        webbrowser.open(
            url
        )

        return (
            f"Opening {site}"
        )

    def get_time(
        self
    ):

        return (

            datetime
            .datetime
            .now()

            .strftime(
                "%I:%M %p"
            )

        )

    def get_date(
        self
    ):

        return (

            datetime
            .datetime
            .now()

            .strftime(
                "%d %B %Y"
            )

        )

    def get_battery(
        self
    ):

        b = (
            psutil
            .sensors_battery()
        )

        if b:

            return (
                f"{b.percent}%"
            )

        return (
            "Unavailable"
        )

    def get_system(
        self
    ):

        return (

            f"CPU "
            f"{psutil.cpu_percent()}%"

        )

    # ==================
    # AI
    # ==================

    def ask_gemini(
        self,
        query
    ):

        if (
            not
            self.client
        ):

            return (
                "AI unavailable."
            )

        try:

            r = (

                self.client

                .models

                .generate_content(

                    model=
                    "gemini-2.5-flash",

                    contents=
                    query

                )

            )

            return (
                r.text
            )

        except Exception as e:

            return str(
                e
            )