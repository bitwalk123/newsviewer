from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QVBoxLayout


class VBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setSpacing(0)

