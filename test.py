import sys
from PySide6.QtCore import Qt, QRectF, QPoint, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QImage, QGuiApplication, QAction
from PySide6.QtWidgets import QApplication, QWidget, QColorDialog

class Whiteboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal Whiteboard")
        self.setMinimumSize(900, 600)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setMouseTracking(True)

        # Canvas
        self.canvas = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        self.canvas.fill(Qt.transparent)

        # Tools/state
        self.active_tool = "pen"       # "pen" | "eraser"
        self.pen_color = QColor("#e6e6e6")
        self.pen_width = 4
        self.drawing = False
        self.last_pos = QPoint()

        # Toolbar / slider state
        self.toolbar_rect = QRectF()
        self.slider_visible = False
        self.slider_rect = QRectF()
        self.slider_dragging = False

        # History (fast: store image snapshots)
        self.history = []
        self.redo_stack = []
        self.max_history = 25
        self._push_history()  # initial state

        # Keyboard shortcuts (optional)
        self.addAction(self._make_shortcut("Ctrl+Z", self.undo))
        self.addAction(self._make_shortcut("Ctrl+Shift+Z", self.redo))
        self.addAction(self._make_shortcut("Ctrl+Y", self.redo))
        self.addAction(self._make_shortcut("Ctrl+K", self.clear_canvas))

    # ---------- helpers ----------
    def _make_shortcut(self, keyseq, slot):
        act = QAction(self)
        act.setShortcut(keyseq)
        act.triggered.connect(slot)
        return act

    def _push_history(self):
        # keep a copy of current canvas
        self.history.append(self.canvas.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.redo_stack.clear()

    # ---------- tool actions ----------
    def set_pen(self):
        if self.active_tool == "pen":
            # toggle slider visibility
            self.slider_visible = not self.slider_visible
        else:
            self.active_tool = "pen"
            self.slider_visible = False
        self.update()

    def set_eraser(self):
        self.active_tool = "eraser"
        self.slider_visible = False
        self.update()

    def clear_canvas(self):
        self.canvas.fill(Qt.transparent)
        self._push_history()
        self.update()

    def undo(self):
        if len(self.history) > 1:
            # move current to redo, revert to previous
            self.redo_stack.append(self.history.pop())
            self.canvas = self.history[-1].copy()
            self.update()

    def redo(self):
        if self.redo_stack:
            img = self.redo_stack.pop()
            self.history.append(img.copy())
            self.canvas = img
            self.update()

    def pick_color(self):
        c = QColorDialog.getColor(self.pen_color, self, "Pick Color")
        if c.isValid():
            self.pen_color = c
            self.update()

    # ---------- layout of toolbar/slider ----------
    def _compute_toolbar_rect(self):
        w = 420.0  # bar width
        h = 48.0
        margin_bottom = 22.0
        x = (self.width() - w) / 2.0
        y = self.height() - h - margin_bottom
        self.toolbar_rect = QRectF(x, y, w, h)

    def _compute_slider_rect(self):
        # appears above toolbar, same center width, wider
        w = 260.0
        h = 40.0
        gap = 10.0
        tb = self.toolbar_rect
        x = tb.center().x() - w / 2.0
        y = tb.top() - gap - h
        self.slider_rect = QRectF(x, y, w, h)

    # ---------- painting ----------
    def paintEvent(self, _):
        # background (dark, like your mock)
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#1f1f28"))  # deep slate
        # subtle border
        p.setPen(QColor("#247ca3"))
        p.drawRect(self.rect().adjusted(0, 0, -1, -1))

        # draw current canvas
        p.drawImage(0, 0, self.canvas)

        # toolbar
        self._compute_toolbar_rect()
        self._compute_slider_rect()
        self._paint_toolbar(p)
        if self.slider_visible:
            self._paint_slider(p)

    def _paint_toolbar(self, p: QPainter):
        r = self.toolbar_rect
        # bg
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(r, 14, 14)

        # buttons layout (6 icons)
        padding = 12
        btn_w = 48
        gap = 8
        x = r.x() + padding
        y = r.y() + (r.height() - btn_w) / 2

        # define buttons & store for hit test
        self.btn_rects = {}
        names = ["pen", "eraser", "clear", "undo", "redo", "color"]
        for name in names:
            rect = QRectF(x, y, btn_w, btn_w)
            self.btn_rects[name] = rect
            self._paint_icon(p, name, rect,
                             active=(name == self.active_tool) if name in ["pen", "eraser"] else False)
            x += btn_w + gap

    def _paint_icon(self, p: QPainter, name: str, rect: QRectF, active=False):
        # draw highlight ring for active tool
        if active:
            p.setBrush(QColor(90, 160, 255, 35))
            p.setPen(Qt.NoPen)
            p.drawEllipse(rect.adjusted(4, 4, -4, -4))

        # icon strokes
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
            # palette circle with current color
            p.setBrush(self.pen_color)
            p.setPen(QPen(QColor("#e6e6e6"), 1))
            p.drawEllipse(rect.adjusted(12, 12, -12, -12))

    def _paint_slider(self, p: QPainter):
        r = self.slider_rect
        # bg
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 44, 52, 220))
        p.drawRoundedRect(r, 12, 12)

        # track
        track = r.adjusted(16, r.height()/2 - 3, -16, -r.height()/2 + 3)
        p.setBrush(QColor(90, 95, 110, 240))
        p.drawRoundedRect(track, 3, 3)

        # handle position maps width [1..30]
        min_w, max_w = 1, 30
        tmin = track.left()
        tmax = track.right()
        tpos = tmin + (tmax - tmin) * ((self.pen_width - min_w) / (max_w - min_w))
        handle = QRectF(tpos - 8, track.center().y() - 10, 16, 20)

        p.setBrush(QColor(230, 230, 230))
        p.drawRoundedRect(handle, 5, 5)

        # preview dot
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#e6e6e6"))
        p.drawEllipse(QPointF(r.right()-28, r.center().y()), self.pen_width/2, self.pen_width/2)

    # ---------- mouse ----------
    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return

        pos = e.position().toPoint()

        # Slider?
        if self.slider_visible and self.slider_rect.contains(pos):
            self.slider_dragging = True
            self._update_slider_from_pos(pos.x())
            return

        # Toolbar buttons?
        if self.toolbar_rect.contains(pos):
            for name, rect in self.btn_rects.items():
                if rect.contains(pos):
                    if name == "pen":
                        self.set_pen()
                    elif name == "eraser":
                        self.set_eraser()
                    elif name == "clear":
                        self.clear_canvas()
                    elif name == "undo":
                        self.undo()
                    elif name == "redo":
                        self.redo()
                    elif name == "color":
                        self.pick_color()
                    return
            return

        # Drawing on canvas
        self.drawing = True
        self.last_pos = pos
        self._draw_to(pos)  # start point

    def mouseMoveEvent(self, e):
        pos = e.position().toPoint()

        if self.slider_dragging:
            self._update_slider_from_pos(pos.x())
            return

        if self.drawing:
            self._draw_to(pos)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.drawing:
                self.drawing = False
                self._push_history()
            self.slider_dragging = False

    def _update_slider_from_pos(self, x):
        track = self.slider_rect.adjusted(16, self.slider_rect.height()/2 - 3, -16, -self.slider_rect.height()/2 + 3)
        x = max(track.left(), min(x, track.right()))
        t = (x - track.left()) / max(1.0, (track.width()))
        self.pen_width = int(1 + t * (30 - 1))
        self.update()

    # ---------- drawing to QImage ----------
    def _draw_to(self, pos: QPoint):
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
        self.update(QRectF(self.last_pos, pos).toRect().adjusted(-50, -50, 50, 50))

    # ---------- resize ----------
    def resizeEvent(self, _):
        if self.canvas.size() != self.size():
            new_img = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
            new_img.fill(Qt.transparent)
            p = QPainter(new_img)
            p.drawImage(0, 0, self.canvas)
            p.end()
            self.canvas = new_img

    # ---------- optional: right click toggles slider when pen active ----------
    def contextMenuEvent(self, _):
        if self.active_tool == "pen":
            self.slider_visible = not self.slider_visible
            self.update()


if __name__ == "__main__":
    QGuiApplication.setApplicationDisplayName("Whiteboard")
    app = QApplication(sys.argv)
    w = Whiteboard()
    w.show()
    sys.exit(app.exec())
