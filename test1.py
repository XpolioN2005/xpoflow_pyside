import json
import sys
from pathlib import Path
from typing import List, Dict

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QInputDialog,
    QLineEdit,
    QMenu,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QFrame,
)


# ----------------------------- Card Widget ----------------------------- #
class CardItem(QListWidgetItem):
    def __init__(self, title: str, description: str = ""):
        super().__init__(title)
        self.setToolTip(description or title)
        # Store structured data for future extensibility
        self.setData(Qt.UserRole, {"title": title, "description": description})
        # Visuals
        self.setSizeHint(QSize(self.sizeHint().width(), 44))

    @property
    def title(self) -> str:
        data = self.data(Qt.UserRole) or {}
        return data.get("title", self.text())

    @property
    def description(self) -> str:
        data = self.data(Qt.UserRole) or {}
        return data.get("description", "")

    def update(self, title: str, description: str):
        self.setText(title)
        self.setToolTip(description or title)
        self.setData(Qt.UserRole, {"title": title, "description": description})


# ----------------------------- Column Widget ----------------------------- #
class KanbanList(QListWidget):
    dropped = Signal()  # emitted after a successful drop to trigger autosave, etc.

    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSpacing(6)
        self.setFrameShape(QFrame.NoFrame)
        self.setAlternatingRowColors(False)
        self.setStyleSheet(
            """
            QListWidget {
                background: #0f1115;
                border: 1px solid #2a2f3a;
                border-radius: 14px;
                padding: 10px;
            }
            QListWidget::item {
                background: #1a1f29;
                border: 1px solid #2f3542;
                border-radius: 10px;
                margin: 2px;
                padding: 10px 12px;
                color: #d6e2ff;
            }
            QListWidget::item:selected {
                background: #283044;
                border: 1px solid #4e5b78;
            }
            QListWidget::item:hover { background: #222938; }
            """
        )

    def dropEvent(self, event):
        super().dropEvent(event)
        self.dropped.emit()


class ColumnWidget(QWidget):
    changed = Signal()  # any mutation (add/edit/remove/drop)

    def __init__(self, title: str = "Todo"):
        super().__init__()
        self.title = title

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #e6ecff; padding: 0 4px;"
        )

        self.add_btn = QPushButton("+")
        self.add_btn.setFixedWidth(32)
        self.add_btn.setToolTip("Add card")
        self.add_btn.clicked.connect(self.add_card_dialog)
        self.add_btn.setStyleSheet(
            """
            QPushButton { background:#3a5cff; color:white; border:none; border-radius:10px; padding:6px; }
            QPushButton:hover { background:#5674ff; }
            QPushButton:pressed { background:#2c48d6; }
            """
        )

        header = QHBoxLayout()
        header.addWidget(self.title_label)
        header.addStretch(1)
        header.addWidget(self.add_btn)

        self.list = KanbanList()
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.open_item_menu)
        self.list.dropped.connect(self.changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addLayout(header)
        layout.addWidget(self.list)

        self.setStyleSheet(
            """
            QWidget#ColumnCard { background:#0b0d12; }
            """
        )

        wrapper = QVBoxLayout()

    # ----- Card actions ----- #
    def add_card(self, title: str, description: str = ""):
        item = CardItem(title, description)
        self.list.addItem(item)
        self.changed.emit()

    def add_card_dialog(self):
        title, ok = QInputDialog.getText(self, "New Card", "Title:")
        if not ok or not title.strip():
            return
        desc, _ = QInputDialog.getMultiLineText(self, "New Card", "Description:")
        self.add_card(title.strip(), desc.strip())

    def open_item_menu(self, pos):
        item = self.list.itemAt(pos)
        menu = QMenu(self)

        if item:
            edit_act = QAction("Edit", self)
            del_act = QAction("Delete", self)
            menu.addAction(edit_act)
            menu.addAction(del_act)

            edit_act.triggered.connect(lambda: self.edit_item(item))
            del_act.triggered.connect(lambda: self.delete_item(item))
        else:
            add_act = QAction("Add Card", self)
            menu.addAction(add_act)
            add_act.triggered.connect(self.add_card_dialog)

        menu.exec(self.list.mapToGlobal(pos))

    def edit_item(self, item: CardItem):
        title, ok = QInputDialog.getText(self, "Edit Card", "Title:", QLineEdit.Normal, item.title)
        if not ok or not title.strip():
            return
        desc, _ = QInputDialog.getMultiLineText(self, "Edit Card", "Description:", item.description)
        item.update(title.strip(), desc.strip())
        self.changed.emit()

    def delete_item(self, item: CardItem):
        row = self.list.row(item)
        self.list.takeItem(row)
        self.changed.emit()

    # ----- Serialization ----- #
    def to_dict(self) -> Dict:
        cards = []
        for i in range(self.list.count()):
            it: CardItem = self.list.item(i)
            data = it.data(Qt.UserRole) or {}
            cards.append(data)
        return {"title": self.title_label.text(), "cards": cards}

    def from_dict(self, data: Dict):
        self.title = data.get("title", self.title)
        self.title_label.setText(self.title)
        self.list.clear()
        for c in data.get("cards", []):
            self.add_card(c.get("title", "Untitled"), c.get("description", ""))


# ----------------------------- Board Widget ----------------------------- #
class BoardWidget(QWidget):
    changed = Signal()  # bubble up from columns

    def __init__(self, columns: List[str] = None):
        super().__init__()
        self.setObjectName("Board")
        self.columns: List[ColumnWidget] = []

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("QScrollArea { border: none; }")

        self.inner = QWidget()
        self.hbox = QHBoxLayout(self.inner)
        self.hbox.setContentsMargins(14, 14, 14, 14)
        self.hbox.setSpacing(16)
        self.hbox.addStretch(1)

        self.scroll.setWidget(self.inner)

        root = QVBoxLayout(self)
        root.addWidget(self.scroll)

        if not columns:
            columns = ["Todo", "Doing", "Done"]
        for name in columns:
            self.add_column(name)

        self.setStyleSheet(
            """
            QWidget#Board { background: #07090d; }
            """
        )

    def add_column(self, title: str):
        col = ColumnWidget(title)
        col.changed.connect(self.changed)

        # Card-like container around the list
        container = QFrame()
        container.setFrameShape(QFrame.NoFrame)
        container.setStyleSheet(
            """
            QFrame { background:#0c111b; border:1px solid #1f2633; border-radius:16px; }
            """
        )
        v = QVBoxLayout(container)
        v.setContentsMargins(10, 10, 10, 10)
        v.addWidget(col)

        self.hbox.insertWidget(self.hbox.count() - 1, container, 0)
        self.columns.append(col)
        self.changed.emit()

    def remove_empty_column(self, index: int):
        if 0 <= index < len(self.columns):
            col = self.columns[index]
            if col.list.count() == 0:
                container = self.hbox.itemAt(index).widget()
                container.deleteLater()
                self.columns.pop(index)
                self.changed.emit()

    def to_dict(self) -> Dict:
        return {"columns": [c.to_dict() for c in self.columns]}

    def from_dict(self, data: Dict):
        # Clear existing columns (keep at least one)
        for i in reversed(range(self.hbox.count()-1)):
            w = self.hbox.itemAt(i).widget()
            if w:
                w.deleteLater()
        self.columns.clear()

        for col in data.get("columns", []):
            self.add_column(col.get("title", "Untitled"))
            self.columns[-1].from_dict(col)
        if not self.columns:
            for name in ("Todo", "Doing", "Done"):
                self.add_column(name)
        self.changed.emit()


# ----------------------------- Main Window ----------------------------- #
class MainWindow(QMainWindow):
    AUTOSAVE_FILE = Path.home() / ".kanban_pyside6.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanban — PySide6")
        self.resize(1100, 650)

        self.board = BoardWidget(["Todo", "Doing", "Done"]) 
        self.board.changed.connect(self.autosave)
        self.setCentralWidget(self.board)

        self._build_menu()
        self._apply_app_style()
        self.load_autosave()

    # ----- Menu / Actions ----- #
    def _build_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        new_act = QAction("New Board", self)
        open_act = QAction("Open…", self)
        save_act = QAction("Save As…", self)
        exit_act = QAction("Exit", self)
        file_menu.addActions([new_act, open_act, save_act])
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        col_menu = menubar.addMenu("Columns")
        add_col_act = QAction("Add Column", self)
        remove_col_act = QAction("Remove Empty Columns", self)
        col_menu.addAction(add_col_act)
        col_menu.addAction(remove_col_act)

        # Wire
        new_act.triggered.connect(self.new_board)
        open_act.triggered.connect(self.open_board)
        save_act.triggered.connect(self.save_board_as)
        exit_act.triggered.connect(self.close)

        add_col_act.triggered.connect(self.prompt_add_column)
        remove_col_act.triggered.connect(self.remove_empty_columns)

    def _apply_app_style(self):
        self.setStyleSheet(
            """
            QMainWindow { background: #07090d; }
            QMenuBar { background:#0c111b; color:#c9d7ff; }
            QMenuBar::item:selected { background:#1b2232; }
            QMenu { background:#0c111b; color:#e6ecff; border:1px solid #1f2633; }
            QMenu::item:selected { background:#1b2232; }
            QLabel { color:#cfe1ff; }
            """
        )

    # ----- File operations ----- #
    def new_board(self):
        self.board.from_dict({"columns": [{"title": "Todo", "cards": []}, {"title": "Doing", "cards": []}, {"title": "Done", "cards": []}]})
        self.autosave()

    def open_board(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Board", str(Path.home()), "Kanban JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.board.from_dict(data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")

    def save_board_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Board As", str(Path.home() / "kanban.json"), "Kanban JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.board.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    def autosave(self):
        try:
            with open(self.AUTOSAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.board.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # best-effort autosave

    def load_autosave(self):
        if self.AUTOSAVE_FILE.exists():
            try:
                with open(self.AUTOSAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.board.from_dict(data)
            except Exception:
                pass

    # ----- Column mgmt ----- #
    def prompt_add_column(self):
        name, ok = QInputDialog.getText(self, "Add Column", "Column title:")
        if ok and name.strip():
            self.board.add_column(name.strip())
            self.autosave()

    def remove_empty_columns(self):
        # Remove from rightmost to leftmost to keep indices stable
        for i in reversed(range(len(self.board.columns))):
            self.board.remove_empty_column(i)
        self.autosave()


# ----------------------------- Entrypoint ----------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # High-DPI friendliness
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())
