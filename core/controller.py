import os
import subprocess
import webbrowser
import pyautogui


class PCController:

    def execute(
        self,
        command
    ):

        cmd = command.lower()

        # =====================
        # SEARCH
        # =====================

        if (
            "search youtube "
            in cmd
        ):

            q = (
                cmd.replace(
                    "search youtube ",
                    ""
                )
            )

            webbrowser.open(

                "https://youtube.com/results?search_query="
                +
                q
            )

            return (
                f"Searching YouTube for {q}"
            )

        if (
            "search google "
            in cmd
        ):

            q = (
                cmd.replace(
                    "search google ",
                    ""
                )
            )

            webbrowser.open(

                "https://google.com/search?q="
                +
                q
            )

            return (
                f"Searching Google for {q}"
            )

        # =====================
        # OPEN
        # =====================

        apps = {

            "chrome":
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            "spotify":
            "spotify",

            "notepad":
            "notepad",

            "calculator":
            "calc",

            "paint":
            "mspaint"
        }

        for app in apps:

            if (
                f"open {app}"
                in cmd
            ):

                subprocess.Popen(
                    apps[app]
                )

                return (
                    f"Opening {app}"
                )

        # =====================
        # FOLDERS
        # =====================

        if (
            "open folder downloads"
            in cmd
        ):

            path = (
                os.path.expanduser(
                    "~/Downloads"
                )
            )

            os.startfile(
                path
            )

            return (
                "Opening Downloads"
            )

        # =====================
        # SCREENSHOT
        # =====================

        if (
            "take screenshot"
            in cmd
        ):

            img = (
                pyautogui
                .screenshot()
            )

            img.save(
                "screenshot.png"
            )

            return (
                "Screenshot saved"
            )

        # =====================
        # TYPE
        # =====================

        if (
            cmd.startswith(
                "type "
            )
        ):

            text = (
                cmd.replace(
                    "type ",
                    ""
                )
            )

            pyautogui.write(
                text,
                interval=0.03
            )

            return (
                "Typed text"
            )

        # =====================
        # CLOSE APP
        # =====================

        if (
            "close chrome"
            in cmd
        ):

            os.system(
                "taskkill /f /im chrome.exe"
            )

            return (
                "Chrome closed"
            )

        return None