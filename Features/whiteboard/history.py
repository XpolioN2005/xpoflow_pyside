from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

class HistoryMixin:
    def _push_history(self):
        self.history.append(self.canvas.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.canvas = self.history[-1].copy()
            self.update()

    def redo(self):
        if self.redo_stack:
            img = self.redo_stack.pop()
            self.history.append(img.copy())
            self.canvas = img
            self.update()
