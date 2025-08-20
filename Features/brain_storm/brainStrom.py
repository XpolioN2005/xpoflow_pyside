from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
)

from Features.brain_storm.textCanvas import TextCanvas
from Utils.load_stylesheet import load_stylesheet

class BrainStorm(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		
		self.setStyleSheet(load_stylesheet("UI/stylesheet/navbar.qss"))

		# Top Nav
		nav = QHBoxLayout()
		self.home_btn = QPushButton("Home")
		self.settings_btn = QPushButton("chat")
		nav.addWidget(self.home_btn)
		nav.addWidget(self.settings_btn)

		# Stacked pages
		self.stacked = QStackedWidget()
		self.stacked.addWidget(TextCanvas())
		self.stacked.addWidget(QLabel("chat with mr ai"))

		layout.addLayout(nav)
		layout.addWidget(self.stacked)
		self.setLayout(layout)

		# Switch pages
		self.home_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
		self.settings_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(1))

