from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel
)

from PyQt6.QtCore import (
    pyqtSignal,
    Qt
)

from ui.orb import JarvisOrb


class MainWindow(QWidget):

    send_message = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.resize(
            950,
            700
        )

        self.setWindowTitle(
            "JARVIS"
        )

        self.setStyleSheet(
            """
            QWidget{
                background:#050A12;
                color:white;
            }

            QTextEdit{
                background:#101820;
                border:none;
                border-radius:12px;
                padding:10px;
            }

            QLineEdit{
                background:#111F30;
                border-radius:10px;
                padding:10px;
            }

            QPushButton{
                background:#00BFFF;
                border-radius:10px;
                padding:10px;
            }
            """
        )

        layout = QVBoxLayout()

        self.orb = JarvisOrb()

        self.orb.setMinimumHeight(
            300
        )

        self.status = QLabel(
            "ONLINE"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.chat = QTextEdit()

        self.chat.setReadOnly(
            True
        )

        self.input = QLineEdit()

        self.send = QPushButton(
            "SEND"
        )

        row = (
            QHBoxLayout()
        )

        row.addWidget(
            self.input
        )

        row.addWidget(
            self.send
        )

        layout.addWidget(
            self.orb
        )

        layout.addWidget(
            self.status
        )

        layout.addWidget(
            self.chat
        )

        layout.addLayout(
            row
        )

        self.setLayout(
            layout
        )

        self.send.clicked.connect(
            self.emit_message
        )

        self.input.returnPressed.connect(
            self.emit_message
        )

    def emit_message(self):

        text = (
            self.input.text()
            .strip()
        )

        if text:

            self.send_message.emit(
                text
            )

            self.input.clear()

    def add_log(
        self,
        text
    ):

        self.chat.append(
            text
        )

    def set_status(
        self,
        text
    ):

        self.status.setText(
            text
        )