from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)

from Features.brain_storm.textCanvas import TextCanvas
from Utils.load_stylesheet import load_stylesheet
from Utils.idea_generator import generate_game_parts


class BrainStorm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        self.setStyleSheet(load_stylesheet("UI/stylesheet/navbar.qss"))

        # --- Header bar with idea + regenerate button ---
        header = QHBoxLayout()

        self.idea = QLabel()
        self.idea.setWordWrap(True)
        self.idea.setAlignment(Qt.AlignCenter)
        self.idea.setTextFormat(Qt.RichText)

        regen_btn = QPushButton("🎲 Regenerate")
        regen_btn.clicked.connect(self.regenerate_idea)

        header.addWidget(self.idea, 1)
        header.addWidget(regen_btn, 0, Qt.AlignRight)

        # --- Main text canvas ---
        self.textcanvas = TextCanvas()

        layout.addLayout(header)
        layout.addWidget(self.textcanvas, 1)
        self.setLayout(layout)

        # First idea
        self.regenerate_idea()

    def regenerate_idea(self):
        parts = generate_game_parts()
        # 🔑 assemble HTML string with highlights
        html = (
            f"A <span style='color:#FFEB3B; font-weight:bold;'>{parts['art_style']}</span> "
            f"style <span style='color:#E91E63; font-weight:bold;'>{parts['genre']}</span> game "
            f"that takes place <span style='color:#03A9F4; font-weight:bold;'>{parts['setting']}</span>, "
            f"where the goal is to <span style='color:#FF5722; font-weight:bold;'>{parts['goal']}</span>. "
            f"But, <span style='color:#9C27B0; font-weight:bold;'>{parts['twist']}</span>. "
            f"Bonus: <span style='color:#4CAF50; font-weight:bold;'>{parts['bonus']}</span>."
        )
        self.idea.setText(html)
