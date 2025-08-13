import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from whiteboard import Whiteboard

if __name__ == "__main__":
    QGuiApplication.setApplicationDisplayName("Whiteboard")
    app = QApplication(sys.argv)
    w = Whiteboard()
    w.show()
    sys.exit(app.exec())
