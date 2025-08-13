# toolbar.py
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

class Toolbar(QWidget):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self.slider_visible = False
        self.slider_dragging = False
        self.btn_rects = {}

        self.setFixedHeight(60)  # toolbar height
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        # Toolbar background
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 14, 14)

        # Buttons
        padding, btn_w, gap = 12, 48, 8
        x = padding
        y = (self.height() - btn_w) / 2
        self.btn_rects.clear()

        names = ["pen", "eraser", "clear", "undo", "redo", "color"]
        for name in names:
            rect = QRectF(x, y, btn_w, btn_w)
            self.btn_rects[name] = rect
            self.paint_icon(p, name, rect,
                active=(name == self.core.active_tool) if name in ["pen", "eraser"] else False)
            x += btn_w + gap

    def paint_icon(self, p: QPainter, name, rect, active=False):
        if active:
            p.setBrush(QColor(90, 160, 255, 35))
            p.setPen(Qt.NoPen)
            p.drawEllipse(rect.adjusted(4, 4, -4, -4))

        p.setPen(QPen(QColor("#e6e6e6"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        cx, cy = rect.center().x(), rect.center().y()
        w, h = rect.width(), rect.height()

        if name == "pen":
            p.drawLine(QPointF(cx - w*0.25, cy + h*0.2), QPointF(cx + w*0.25, cy - h*0.2))
            p.drawLine(QPointF(cx + w*0.05, cy - h*0.23), QPointF(cx + w*0.25, cy - h*0.03))
        elif name == "eraser":
            p.drawRect(rect.adjusted(w*0.25, h*0.25, -w*0.25, -h*0.25))
        elif name == "clear":
            p.drawLine(rect.topLeft() + QPointF(8, 8), rect.bottomRight() - QPointF(8, 8))
            p.drawLine(rect.bottomLeft() + QPointF(8, -8), rect.topRight() - QPointF(8, -8))
        elif name == "undo":
            p.drawArc(rect.adjusted(10, 12, -6, -8), 40*16, 280*16)
            p.drawLine(QPointF(rect.left()+12, cy), QPointF(rect.left()+20, cy-8))
        elif name == "redo":
            p.drawArc(rect.adjusted(6, 12, -10, -8), 120*16, -280*16)
            p.drawLine(QPointF(rect.right()-12, cy), QPointF(rect.right()-20, cy-8))
        elif name == "color":
            p.setBrush(self.core.pen_color)
            p.setPen(QPen(QColor("#e6e6e6"), 1))
            p.drawEllipse(rect.adjusted(12, 12, -12, -12))
