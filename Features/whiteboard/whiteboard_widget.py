import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QAction
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from .whiteboard_core import WhiteboardCore
from .whiteboard_toolbar import Toolbar


class WhiteboardCanvas(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setMouseTracking(True)

    def paintEvent(self, _):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#1f1f28"))
        p.setPen(QColor("#247ca3"))
        p.drawRect(self.rect().adjusted(0, 0, -1, -1))
        p.drawImage(0, 0, self.core.canvas)

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        self.core.start_drawing(e.position().toPoint())
        self.update()

    def mouseMoveEvent(self, e):
        self.core.draw_move(e.position().toPoint())
        self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.core.end_drawing()
            self.update()

    def resizeEvent(self, _):
        self.core.resize_canvas(self.size())


class WhiteboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whiteboard with Toolbar")
        self.setMinimumSize(900, 600)

        self.core = WhiteboardCore(self)
        self.toolbar = Toolbar(self.core, self)
        self.canvas = WhiteboardCanvas(self.core)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        layout.addWidget(self.toolbar, alignment=Qt.AlignHCenter)
        layout.addWidget(self.canvas)

        # Shortcuts
        self.addAction(self._make_shortcut("Ctrl+Z", self.core.undo))
        self.addAction(self._make_shortcut("Ctrl+Shift+Z", self.core.redo))
        self.addAction(self._make_shortcut("Ctrl+Y", self.core.redo))
        self.addAction(self._make_shortcut("Ctrl+K", self.core.clear_canvas))

    def _make_shortcut(self, keyseq, slot):
        act = QAction(self)
        act.setShortcut(keyseq)
        act.triggered.connect(slot)
        return act


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WhiteboardWidget()
    w.show()
    sys.exit(app.exec())
