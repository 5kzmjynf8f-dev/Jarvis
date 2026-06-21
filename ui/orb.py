from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (
    QPainter,
    QColor
)

from PyQt6.QtCore import (
    QTimer
)


class JarvisOrb(QWidget):

    def __init__(self):

        super().__init__()

        self.radius = 85

        self.grow = True

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(
            30
        )

    def animate(self):

        if self.grow:

            self.radius += 1

            if self.radius > 95:

                self.grow = False

        else:

            self.radius -= 1

            if self.radius < 85:

                self.grow = True

        self.update()

    def paintEvent(
        self,
        e
    ):

        p = QPainter(self)

        p.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        center = (
            self.rect()
            .center()
        )

        for i in range(
            5
        ):

            p.setBrush(

                QColor(
                    0,
                    180,
                    255,
                    40
                    -
                    i * 5
                )
            )

            p.drawEllipse(

                center,

                self.radius
                +
                i * 15,

                self.radius
                +
                i * 15
            )