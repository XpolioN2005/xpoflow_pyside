import sys
from PySide6.QtWidgets import (
    QWidget, QTextEdit
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent

from Utils.load_stylesheet import load_stylesheet


class DraggableTextEdit(QTextEdit):
    """A text box that can be dragged and right-clicked to delete."""
    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.canvas = canvas
        self._dragging = False
        self._drag_offset = QPoint()

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
    """A widget where you can tap to add draggable text bubbles."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.text_boxes = []

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            pos = event.position().toPoint()

            # Check if click is on an existing text box
            for tb in self.text_boxes:
                if tb.geometry().contains(pos):
                    return  # Do nothing (handled by the text box itself)

            # Otherwise, add a new one
            self.add_text_box(pos)

    def add_text_box(self, pos: QPoint):
        text_edit = DraggableTextEdit(self, self)
        text_edit.setPlaceholderText("Type here...")
        text_edit.move(pos)
        text_edit.resize(150, 40)
        text_edit.setStyleSheet(load_stylesheet("UI/stylesheet/textField.qss"))
        text_edit.show()
        text_edit.setFocus()
        self.text_boxes.append(text_edit)

