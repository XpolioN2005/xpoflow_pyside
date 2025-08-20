import sys
from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QImage, QAction
from PySide6.QtWidgets import QWidget

from .toolbar import ToolbarMixin
from .slider import SliderMixin
from .tools import ToolsMixin
from .history import HistoryMixin

class Whiteboard(QWidget, ToolbarMixin, SliderMixin, ToolsMixin, HistoryMixin):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Minimal Whiteboard")
		# self.setMinimumSize(900, 600)
		self.setAttribute(Qt.WA_OpaquePaintEvent, True)
		self.setMouseTracking(True)
		self.setStyleSheet("QWidget { outline: none; }")
		self.setFocusPolicy(Qt.NoFocus)


		self.canvas = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
		self.canvas.fill(Qt.transparent)

		self.active_tool = "pen"
		self.pen_color = QColor("#e6e6e6")
		self.pen_width = 4
		self.drawing = False
		self.last_pos = QPoint()

		self.toolbar_rect = QRectF()
		self.slider_visible = False
		self.slider_rect = QRectF()
		self.slider_dragging = False

		self.history = []
		self.redo_stack = []
		self.max_history = 25
		self._push_history()

		self.addAction(self._make_shortcut("Ctrl+Z", self.undo))
		self.addAction(self._make_shortcut("Ctrl+Shift+Z", self.redo))
		self.addAction(self._make_shortcut("Ctrl+Y", self.redo))
		self.addAction(self._make_shortcut("Ctrl+K", self.clear_canvas))

	def _make_shortcut(self, keyseq, slot):
		act = QAction(self)
		act.setShortcut(keyseq)
		act.triggered.connect(slot)
		return act

	def paintEvent(self, _):
		p = QPainter(self)
		p.fillRect(self.rect(), QColor("#18181C"))
		p.setPen(QColor("#1f1f28")) # show think outline but why?
		p.drawRect(self.rect().adjusted(0, 0, -1, -1))

		p.drawImage(0, 0, self.canvas)

		self._compute_toolbar_rect()
		self._compute_slider_rect()
		self._paint_toolbar(p)
		if self.slider_visible:
			self._paint_slider(p)

	def mousePressEvent(self, e):
		if e.button() != Qt.LeftButton:
			return
		pos = e.position().toPoint()

		if self.slider_visible and self.slider_rect.contains(pos):
			self.slider_dragging = True
			self._update_slider_from_pos(pos.x())
			return

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

		self.drawing = True
		self.last_pos = pos
		self._draw_to(pos)

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
		self.update()

	def resizeEvent(self, _):
		if self.canvas.size() != self.size():
			new_img = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
			new_img.fill(Qt.transparent)
			p = QPainter(new_img)
			p.drawImage(0, 0, self.canvas)
			p.end()
			self.canvas = new_img

	def contextMenuEvent(self, _):
		if self.active_tool == "pen":
			self.slider_visible = not self.slider_visible
			self.update()
		
