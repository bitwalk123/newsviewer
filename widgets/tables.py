from PySide6.QtCore import Qt, QMargins
from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView


class TableWidget(QTableWidget):
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                font-family: monospace;
            }
            QHeaderView::section:horizontal {
                font-family: monospace;
            }
            QHeaderView::section:vertical {
                font-family: monospace;
                margin-left: 0.3em;
                margin-right: 0.3em;
            }
        """)
        self.setHorizontalHeaderLabels(["日付", "タイトル"])

        # 行番号を右寄せにする
        self.verticalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # 列の幅調整
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
