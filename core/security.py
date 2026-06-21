import psutil
import platform


class SecurityMonitor:

    def get_report(self):

        cpu = (
            psutil.cpu_percent()
        )

        ram = (
            psutil.virtual_memory()
            .percent
        )

        disk = (
            psutil.disk_usage("/")
            .percent
        )

        processes = len(

            psutil.pids()

        )

        score = 100

        if cpu > 90:
            score -= 20

        if ram > 90:
            score -= 20

        if disk > 95:
            score -= 10

        return {

            "os":
            platform.system(),

            "cpu":
            cpu,

            "ram":
            ram,

            "disk":
            disk,

            "processes":
            processes,

            "score":
            score
        }

    def suspicious(self):

        suspicious = []

        words = [

            "miner",
            "hack",
            "inject",
            "rat",
            "trojan"
        ]

        for p in psutil.process_iter(
            [
                "name"
            ]
        ):

            try:

                name = (

                    p.info[
                        "name"
                    ]
                    .lower()
                )

                if any(

                    x in name

                    for x

                    in words

                ):

                    suspicious.append(
                        name
                    )

            except:
                pass

        return suspicious