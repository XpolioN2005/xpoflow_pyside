from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPen, QPainter
from PySide6.QtSvg import QSvgRenderer

class ToolbarMixin:
	def __init__(self):
		super().__init__()
		self.icons = {}
		for name in ["pen", "eraser", "clear", "undo", "redo"]:
			self.icons[name] = QSvgRenderer(f"assets/icons/{name}.svg")

	def _compute_toolbar_rect(self):
		w = 340.0
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
			self._paint_icon(
				p, name, rect,
				active=(name == self.active_tool) if name in ["pen", "eraser"] else False
			)
			x += btn_w + gap

	def _paint_icon(self, p, name, rect, active=False):
		if active:
			p.setBrush(QColor(90, 160, 255, 35))
			p.setPen(Qt.NoPen)
			p.drawEllipse(rect.adjusted(4, 4, -4, -4))

		icon_margin = 12
		icon_rect = rect.adjusted(icon_margin, icon_margin, -icon_margin, -icon_margin)

		if name == "color":
			p.setBrush(self.pen_color)
			p.setPen(QPen(QColor("#e6e6e6"), 1))
			p.drawEllipse(icon_rect)
		else:
			renderer = self.icons.get(name)
			if renderer and renderer.isValid():
				from PySide6.QtGui import QPixmap

				size = icon_rect.size().toSize()
				# Create high-res transparent buffer
				pixmap = QPixmap(size)
				pixmap.fill(Qt.transparent)

				# Render SVG into pixmap
				temp_painter = QPainter(pixmap)
				temp_painter.setRenderHint(QPainter.Antialiasing, True)
				temp_painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
				renderer.render(temp_painter, QRectF(0, 0, size.width(), size.height()))
				temp_painter.end()

				# Tint the pixmap
				tinted = QPixmap(size)
				tinted.fill(Qt.transparent)
				temp_painter = QPainter(tinted)
				temp_painter.setCompositionMode(QPainter.CompositionMode_Source)
				temp_painter.drawPixmap(0, 0, pixmap)
				temp_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
				temp_painter.fillRect(tinted.rect(), QColor("#e6e6e6"))
				temp_painter.end()

				# Draw tinted pixmap
				p.setRenderHint(QPainter.SmoothPixmapTransform, True)
				p.drawPixmap(icon_rect.topLeft(), tinted)
