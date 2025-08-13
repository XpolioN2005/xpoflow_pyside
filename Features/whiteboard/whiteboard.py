
# from PySide6.QtWidgets import QWidget, QVBoxLayout
# from .whiteboard_widget import WhiteboardWidget
# from .whiteboard_toolbar import WhiteboardToolbar

# class Whiteboard(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout(self)
#         self.toolbar = WhiteboardToolbar()
#         self.canvas = WhiteboardWidget()
#         layout.addWidget(self.toolbar)
#         layout.addWidget(self.canvas)

#         # Connect toolbar to canvas
#         self.toolbar.pen_selected.connect(lambda: self.canvas.set_pen_color(self.canvas.current_color))
#         self.toolbar.eraser_selected.connect(self.canvas.set_eraser)
#         self.toolbar.color_changed.connect(self.canvas.set_pen_color)
#         self.toolbar.size_changed.connect(self.canvas.set_pen_size)
#         self.toolbar.undo_requested.connect(self.canvas.undo)
#         self.toolbar.redo_requested.connect(self.canvas.redo)
#         self.toolbar.clear_requested.connect(self.canvas.clear_board)
