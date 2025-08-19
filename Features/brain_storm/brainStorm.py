import sys
from PySide6.QtWidgets import QWidget, QTextEdit
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent

from Utils.load_stylesheet import load_stylesheet


class DraggableTextEdit(QTextEdit):
	"""A text box that can be dragged, auto-resized, and right-clicked to delete."""
	def __init__(self, parent, canvas, max_width=300, max_height=200):
		super().__init__(parent)
		self.canvas = canvas
		self._dragging = False
		self._drag_offset = QPoint()
		self.max_width = max_width
		self.max_height = max_height

		# Auto-resize when text changes
		self.textChanged.connect(self.auto_resize)

	def auto_resize(self):
		"""Only grow when text starts overflowing."""
		doc_size = self.document().size().toSize()

		# Clamp to max dimensions
		needed_height = min(self.max_height, doc_size.height()+10)

		self.resize( self.width(), needed_height)



	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.RightButton:
			# Right-click deletes this text box
			if self in self.canvas.text_boxes:
				self.canvas.text_boxes.remove(self)
			self.deleteLater()
		elif event.button() == Qt.LeftButton:
			# Left-click starts dragging
			self._dragging = True
			self._drag_offset = event.position().toPoint()
		super().mousePressEvent(event)

	def mouseMoveEvent(self, event: QMouseEvent):
		if self._dragging:
			new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
			self.move(new_pos)

	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.LeftButton:
			self._dragging = False
		super().mouseReleaseEvent(event)


class TextCanvas(QWidget):
	"""A widget where you can tap to add draggable, auto-resizing text bubbles."""
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAttribute(Qt.WA_StyledBackground, True)
		self.setStyleSheet("background-color: #18181C;")
		self.text_boxes = []

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.LeftButton:
			pos = event.position().toPoint()

			# Check if click is on an existing text box
			for tb in self.text_boxes:
				if tb.geometry().contains(pos):
					return  # Click belongs to text box → don't spawn new

			# Otherwise, add a new one
			self.add_text_box(pos)

	def add_text_box(self, pos: QPoint):
		text_edit = DraggableTextEdit(self, self, max_width=300, max_height=200)
		text_edit.setPlaceholderText("Type here...")
		text_edit.move(pos)
		text_edit.resize(250, 40)
		text_edit.setStyleSheet(load_stylesheet("UI/stylesheet/textField.qss"))
		text_edit.show()
		text_edit.setFocus()
		self.text_boxes.append(text_edit)
