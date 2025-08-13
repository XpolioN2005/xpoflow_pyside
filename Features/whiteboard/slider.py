from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QColor,QPainter

class SliderMixin:
    def _compute_slider_rect(self):
        w = 260.0
        h = 40.0
        gap = 10.0
        tb = self.toolbar_rect
        x = tb.center().x() - w / 2.0
        y = tb.top() - gap - h
        self.slider_rect = QRectF(x, y, w, h)

    def _paint_slider(self, p):
        r = self.slider_rect
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(r, 12, 12)

        track = r.adjusted(16, r.height()/2 - 3, -16, -r.height()/2 + 3)
        p.setBrush(QColor(90, 95, 110, 240))
        p.drawRoundedRect(track, 3, 3)

        min_w, max_w = 1, 30
        tmin = track.left()
        tmax = track.right()
        tpos = tmin + (tmax - tmin) * ((self.pen_width - min_w) / (max_w - min_w))
        handle = QRectF(tpos - 8, track.center().y() - 10, 16, 20)

        p.setBrush(QColor(230, 230, 230))
        p.drawRoundedRect(handle, 5, 5)

        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#e6e6e6"))
        p.drawEllipse(QPointF(r.right()-28, r.center().y()), self.pen_width/2, self.pen_width/2)

    def _update_slider_from_pos(self, x):
        track = self.slider_rect.adjusted(16, self.slider_rect.height()/2 - 3, -16, -self.slider_rect.height()/2 + 3)
        x = max(track.left(), min(x, track.right()))
        t = (x - track.left()) / max(1.0, (track.width()))
        self.pen_width = int(1 + t * (30 - 1))
        self.update()
