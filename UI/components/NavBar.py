from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QScrollArea, QFrame
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon

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
        self.setFixedWidth(135)
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

        # Helper to make button with icon + text
        def make_btn(icon_path, text, slot):
            btn = QPushButton(text)
            btn.setIcon(QIcon(f"assets/icons/{icon_path}.svg"))
            btn.setIconSize(QSize(20, 20))  # adjust size as needed
            btn.clicked.connect(slot)
            return btn

        btn_home = make_btn("home", "Home", self.homeClicked.emit)
        top_layout.addWidget(btn_home)

        btn_projects = make_btn("projects", "Projects", self.projectsClicked.emit)
        top_layout.addWidget(btn_projects)

        btn_brainstorm = make_btn("brainstorm", "Brainstorm", self.brainstormClicked.emit)
        top_layout.addWidget(btn_brainstorm)

        btn_whiteboard = make_btn("whiteboard", "Whiteboard", self.whiteboardClicked.emit)
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

        btn_settings = make_btn("settings", "Settings", self.settingsClicked.emit)
        bottom_layout.addWidget(btn_settings)

        main_layout.addWidget(bottom)
