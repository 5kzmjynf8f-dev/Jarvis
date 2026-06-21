from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLineEdit

class PinUnlock:
 
 PIN = "PROJECTJARVIS001"

 def authenticate(self):

    pin, ok = QInputDialog.getText(
        None,
        "JARVIS",
        "Enter PIN:",
        QLineEdit.EchoMode.Password
    )

    if not ok:
        return False

    return pin == self.PIN
