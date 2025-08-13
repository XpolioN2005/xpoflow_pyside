# test_whiteboard.py

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from Features import Whiteboard

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whiteboard Test")
        self.resize(900, 700)

        layout = QVBoxLayout(self)

        # Create whiteboard controller (handles widget + toolbar)
        self.whiteboard_controller = Whiteboard()

        layout.addWidget(self.whiteboard_controller)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
