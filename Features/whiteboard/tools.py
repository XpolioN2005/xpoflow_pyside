from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import Qt

class ToolsMixin:
    def set_pen(self):
        if self.active_tool == "pen":
            self.slider_visible = not self.slider_visible
        else:
            self.active_tool = "pen"
            self.slider_visible = False
        self.update()

    def set_eraser(self):
        if self.active_tool == "eraser":
            self.slider_visible = not self.slider_visible
        else:
            self.active_tool = "eraser"
            self.slider_visible = False
        self.update()

    def clear_canvas(self):
        self.canvas.fill(Qt.transparent)
        self._push_history()
        self.update()

    def pick_color(self):
        c = QColorDialog.getColor(self.pen_color, self, "Pick Color")
        if c.isValid():
            self.pen_color = c
            self.update()
