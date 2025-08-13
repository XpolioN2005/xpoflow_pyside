from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QColor, QPen, QPainter

class ToolbarMixin:
    def _compute_toolbar_rect(self):
        w = 420.0
        h = 48.0
        margin_bottom = 22.0
        x = (self.width() - w) / 2.0
        y = self.height() - h - margin_bottom
        self.toolbar_rect = QRectF(x, y, w, h)

    def _paint_toolbar(self, p):
        r = self.toolbar_rect
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(r, 14, 14)

        padding = 12
        btn_w = 48
        gap = 8
        x = r.x() + padding
        y = r.y() + (r.height() - btn_w) / 2

        self.btn_rects = {}
        names = ["pen", "eraser", "clear", "undo", "redo", "color"]
        for name in names:
            rect = QRectF(x, y, btn_w, btn_w)
            self.btn_rects[name] = rect
            self._paint_icon(p, name, rect, active=(name == self.active_tool) if name in ["pen", "eraser"] else False)
            x += btn_w + gap

    def _paint_icon(self, p, name, rect, active=False):
        if active:
            p.setBrush(QColor(90, 160, 255, 35))
            p.setPen(Qt.NoPen)
            p.drawEllipse(rect.adjusted(4, 4, -4, -4))

        p.setPen(QPen(QColor("#e6e6e6"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        cx = rect.center().x()
        cy = rect.center().y()
        w = rect.width()
        h = rect.height()

        if name == "pen":
            p.drawLine(QPointF(cx - w*0.25, cy + h*0.2), QPointF(cx + w*0.25, cy - h*0.2))
            p.drawLine(QPointF(cx + w*0.05, cy - h*0.23), QPointF(cx + w*0.25, cy - h*0.03))
        elif name == "eraser":
            p.drawRect(rect.adjusted(w*0.25, h*0.25, -w*0.25, -h*0.25))
        elif name == "clear":
            p.drawLine(QPointF(rect.left()+8, rect.top()+8), QPointF(rect.right()-8, rect.bottom()-8))
            p.drawLine(QPointF(rect.left()+8, rect.bottom()-8), QPointF(rect.right()-8, rect.top()+8))
        elif name == "undo":
            p.drawArc(rect.adjusted(10, 12, -6, -8), 40*16, 280*16)
            p.drawLine(QPointF(rect.left()+12, cy), QPointF(rect.left()+20, cy-8))
        elif name == "redo":
            p.drawArc(rect.adjusted(6, 12, -10, -8), 120*16, -280*16)
            p.drawLine(QPointF(rect.right()-12, cy), QPointF(rect.right()-20, cy-8))
        elif name == "color":
            p.setBrush(self.pen_color)
            p.setPen(QPen(QColor("#e6e6e6"), 1))
            p.drawEllipse(rect.adjusted(12, 12, -12, -12))
