from PySide6.QtCore import QMargins
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QPushButton, QStyle


class ActionFolder(QAction):
    def __init__(self, parent):
        super().__init__(parent)
        icon_open = parent.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        self.setIcon(icon_open)
        self.setToolTip("ローカルパーサー保管場所")


class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("QPushButton {font-family: monospace;}")
