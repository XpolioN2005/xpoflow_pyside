# # test_navbar.py
# import sys
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
#     QPushButton, QLabel, QSizePolicy, QScrollArea, QFrame
# )
# from PySide6.QtCore import Qt

# class NavBar(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setFixedWidth(200)
#         # MUST request full vertical space from parent
#         self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

#         self.setStyleSheet("""
#             QWidget { background: #1e1e1e; color: white; }
#             QPushButton { background: transparent; border: none; padding: 10px; text-align: left; }
#             QPushButton:hover { background: #2d2d2d; }
#         """)

#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(0,0,0,0)
#         main_layout.setSpacing(0)

#         # ---------- Top: scrollable area for many nav items ----------
#         top_container = QWidget()
#         top_layout = QVBoxLayout(top_container)
#         top_layout.setContentsMargins(0,0,0,0)
#         top_layout.setSpacing(0)

#         # Add many items to prove spacer works
#         for i in range(8):
#             top_layout.addWidget(QPushButton(f"Item {i+1}"))

#         # This stretch in the top container keeps those items packed at top of the scroller
#         top_layout.addStretch(1)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)
#         scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         scroll.setWidget(top_container)

#         main_layout.addWidget(scroll, 1)  # give the scroll area expanding stretch

#         # ---------- Bottom: fixed area that stays at bottom ----------
#         bottom = QWidget()
#         bottom_layout = QVBoxLayout(bottom)
#         bottom_layout.setContentsMargins(8,8,8,8)
#         bottom_layout.addWidget(QPushButton("⚙ Settings"))
#         main_layout.addWidget(bottom)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("NavBar test")
#         self.resize(900, 600)

#         central = QWidget()
#         hl = QHBoxLayout(central)
#         hl.setContentsMargins(0,0,0,0)
#         hl.setSpacing(0)

#         self.navbar = NavBar()
#         hl.addWidget(self.navbar)

#         content = QLabel("Main Content Area")
#         content.setAlignment(Qt.AlignCenter)
#         content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         hl.addWidget(content, 1)

#         self.setCentralWidget(central)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = MainWindow()
#     w.show()
#     sys.exit(app.exec())
