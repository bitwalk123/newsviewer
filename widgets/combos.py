from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("QComboBox {font-family: monospace;}")
