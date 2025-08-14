import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


from UI.components.NavBar import NavBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NavBar test")
        self.resize(900, 600)

        central = QWidget()
        hl = QHBoxLayout(central)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(0)

        self.navbar = NavBar()
        hl.addWidget(self.navbar)

        content = QLabel("Main Content Area")
        content.setAlignment(Qt.AlignCenter)
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hl.addWidget(content, 1)

        self.setCentralWidget(central)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec())
     

     
