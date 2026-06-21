from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton
)

from core.security import (
    SecurityMonitor
)


class SecurityWidget(
    QWidget
):

    def __init__(self):

        super().__init__()

        self.monitor = (
            SecurityMonitor()
        )

        layout = (
            QVBoxLayout()
        )

        self.info = QLabel()

        self.scan = QPushButton(
            "Run Scan"
        )

        layout.addWidget(
            self.info
        )

        layout.addWidget(
            self.scan
        )

        self.setLayout(
            layout
        )

        self.scan.clicked.connect(
            self.refresh
        )

        self.refresh()

    def refresh(
        self
    ):

        r = (
            self.monitor
            .get_report()
        )

        sus = (

            self.monitor
            .suspicious()

        )

        text = f"""
OS: {r['os']}

Security Score:
{r['score']}/100

CPU:
{r['cpu']}%

RAM:
{r['ram']}%

Disk:
{r['disk']}%

Processes:
{r['processes']}

Suspicious:
{len(sus)}
"""

        self.info.setText(
            text
        )