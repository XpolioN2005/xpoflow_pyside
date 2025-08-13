# whiteboard_core.py
from PySide6.QtCore import Qt, QPoint, QRectF
from PySide6.QtGui import QColor, QImage, QPainter, QPen
from PySide6.QtWidgets import QColorDialog

class WhiteboardCore:
    def __init__(self, widget):
        self.widget = widget  # parent widget

        # Canvas
        self.canvas = QImage(widget.size(), QImage.Format_ARGB32_Premultiplied)
        self.canvas.fill(Qt.transparent)

        # State
        self.active_tool = "pen"
        self.pen_color = QColor("#e6e6e6")
        self.pen_width = 4
        self.drawing = False
        self.last_pos = QPoint()

        # History
        self.history = []
        self.redo_stack = []
        self.max_history = 25
        self._push_history()

    # ---------- History ----------
    def _push_history(self):
        self.history.append(self.canvas.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.canvas = self.history[-1].copy()
            self.widget.update()

    def redo(self):
        if self.redo_stack:
            img = self.redo_stack.pop()
            self.history.append(img.copy())
            self.canvas = img
            self.widget.update()

    def clear_canvas(self):
        self.canvas.fill(Qt.transparent)
        self._push_history()
        self.widget.update()

    # ---------- Tools ----------
    def set_pen(self):
        self.active_tool = "pen"

    def set_eraser(self):
        self.active_tool = "eraser"

    def pick_color(self):
        c = QColorDialog.getColor(self.pen_color, self.widget, "Pick Color")
        if c.isValid():
            self.pen_color = c
            self.widget.update()

    # ---------- Drawing ----------
    def start_drawing(self, pos):
        self.drawing = True
        self.last_pos = pos
        self._draw_to(pos)

    def draw_move(self, pos):
        if self.drawing:
            self._draw_to(pos)

    def end_drawing(self):
        if self.drawing:
            self.drawing = False
            self._push_history()

    def _draw_to(self, pos):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self.active_tool == "eraser":
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            pen = QPen(Qt.transparent, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        else:
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        painter.setPen(pen)
        painter.drawLine(self.last_pos, pos)
        painter.end()

        self.last_pos = pos
        self.widget.update(QRectF(self.last_pos, pos).toRect().adjusted(-50, -50, 50, 50))

    # ---------- Resize ----------
    def resize_canvas(self, size):
        if self.canvas.size() != size:
            new_img = QImage(size, QImage.Format_ARGB32_Premultiplied)
            new_img.fill(Qt.transparent)
            p = QPainter(new_img)
            p.drawImage(0, 0, self.canvas)
            p.end()
            self.canvas = new_img
