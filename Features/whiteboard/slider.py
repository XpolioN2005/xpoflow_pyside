from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QColor, QPainter

class SliderMixin:
    def __init__(self):
        super().__init__()
        self.min_w = 1
        self.max_w = 30
        self.pen_width = 5  # default pen size

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

        # Background
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(r, 12, 12)

        # Fixed preview space (max pen width)
        max_preview_radius = self.max_w / 2
        preview_padding = 8
        preview_space = max_preview_radius * 2 + preview_padding * 2

        # Track area (static length)
        track = QRectF(
            r.left() + 16,
            r.center().y() - 3,
            r.width() - 16 - preview_space,
            6
        )
        p.setBrush(QColor(90, 95, 110, 240))
        p.drawRoundedRect(track, 3, 3)

        # Handle position
        tpos = track.left() + track.width() * ((self.pen_width - self.min_w) / (self.max_w - self.min_w))
        handle = QRectF(tpos - 8, track.center().y() - 10, 16, 20)
        p.setBrush(QColor(230, 230, 230))
        p.drawRoundedRect(handle, 5, 5)

        # Preview circle (current size, fixed position)
        preview_center = QPointF(r.right() - max_preview_radius - preview_padding, r.center().y())
        p.setBrush(QColor("#e6e6e6"))
        p.drawEllipse(preview_center, self.pen_width / 2, self.pen_width / 2)

    def _update_slider_from_pos(self, x):
        # Match track length from _paint_slider
        max_preview_radius = self.max_w / 2
        preview_padding = 10
        preview_space = max_preview_radius * 2 + preview_padding * 2

        track = QRectF(
            self.slider_rect.left() + 16,
            self.slider_rect.center().y() - 3,
            self.slider_rect.width() - 16 - preview_space,
            6
        )

        x = max(track.left(), min(x, track.right()-4))
        t = (x - track.left()) / max(1.0, track.width())
        self.pen_width = int(self.min_w + t * (self.max_w - self.min_w))
        self.update()
