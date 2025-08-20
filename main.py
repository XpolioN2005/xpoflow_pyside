import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


from UI.components.NavBar import NavBar
from Features.whiteboard.whiteboard import Whiteboard
from Features.brain_storm.brainStorm import TextCanvas

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("XpoFlow")
		self.resize(900, 600)

		central = QWidget()
		hl = QHBoxLayout(central)
		hl.setContentsMargins(0,0,0,0)
		hl.setSpacing(0)

		self.navbar = NavBar()
		hl.addWidget(self.navbar)

		self.navbar.homeClicked.connect(lambda: self.change_scene("home"))
		self.navbar.projectsClicked.connect(lambda: self.change_scene("projects"))
		self.navbar.brainstormClicked.connect(lambda: self.change_scene("brainstorm"))
		self.navbar.whiteboardClicked.connect(lambda: self.change_scene("whiteboard"))
		self.navbar.settingsClicked.connect(lambda: self.change_scene("settings"))

		self.content = QLabel("Main Content Area")
		self.content.setAlignment(Qt.AlignCenter)
		self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		hl.addWidget(self.content, 1)

		self.setCentralWidget(central)
	
	def change_scene(self, scene: str):
		match scene:
			case "whiteboard":
				new_widget = Whiteboard()
			case "home":
				new_widget = QLabel("🏠 Home Page")
			case "projects":
				new_widget = QLabel("📂 Projects Page")
			case "brainstorm":
				new_widget = TextCanvas()
			case "settings":
				new_widget = QLabel("⚙ Settings Page")
			case _:
				return  # invalid scene, do nothing

		# new_widget.setAlignment(Qt.AlignCenter)
		new_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Get layout and replace the content widget
		layout = self.centralWidget().layout()

		# Remove old content widget
		layout.removeWidget(self.content)
		self.content.deleteLater()

		# Set new widget
		self.content = new_widget
		layout.addWidget(self.content, 1)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec())
	 

	 
