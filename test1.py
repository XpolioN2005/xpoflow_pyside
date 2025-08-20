import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QStackedWidget, QLabel
)


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Top Nav
        nav = QHBoxLayout()
        self.home_btn = QPushButton("Home")
        self.settings_btn = QPushButton("Settings")
        nav.addWidget(self.home_btn)
        nav.addWidget(self.settings_btn)

        # Stacked pages
        self.stacked = QStackedWidget()
        self.stacked.addWidget(QLabel("🏠 Home Screen"))
        self.stacked.addWidget(QLabel("⚙️ Settings Screen"))

        layout.addLayout(nav)
        layout.addWidget(self.stacked)
        self.setLayout(layout)

        # Switch pages
        self.home_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.settings_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(1))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top Nav with Screens")
        self.setCentralWidget(MainScreen())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
