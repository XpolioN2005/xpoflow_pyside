from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QScrollArea, QFrame
from PySide6.QtCore import Qt, Signal

from Utils.load_stylesheet import load_stylesheet

class NavBar(QWidget):
    # Signals for modular handling
    homeClicked = Signal()
    projectsClicked = Signal()
    brainstormClicked = Signal()
    whiteboardClicked = Signal()
    settingsClicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.setStyleSheet(load_stylesheet("UI/stylesheet/navbar.qss"))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------- Top: scrollable nav buttons ----------
        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # Create buttons
        btn_home = QPushButton("🏠 Home")
        btn_home.clicked.connect(self.homeClicked.emit)
        top_layout.addWidget(btn_home)

        btn_projects = QPushButton("📂 Projects")
        btn_projects.clicked.connect(self.projectsClicked.emit)
        top_layout.addWidget(btn_projects)

        btn_brainstorm = QPushButton("💡 Brainstorm")
        btn_brainstorm.clicked.connect(self.brainstormClicked.emit)
        top_layout.addWidget(btn_brainstorm)

        btn_whiteboard = QPushButton("📝 Whiteboard")
        btn_whiteboard.clicked.connect(self.whiteboardClicked.emit)
        top_layout.addWidget(btn_whiteboard)

        # Keep items packed at top
        top_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(top_container)

        main_layout.addWidget(scroll, 1)

        # ---------- Bottom: Settings ----------
        bottom = QWidget()
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        btn_settings = QPushButton("⚙ Settings")
        btn_settings.clicked.connect(self.settingsClicked.emit)
        bottom_layout.addWidget(btn_settings)

        main_layout.addWidget(bottom)
