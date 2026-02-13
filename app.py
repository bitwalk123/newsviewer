import sys
import webbrowser

import requests
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QHeaderView,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from bs4 import BeautifulSoup

# 基底クラスとパッケージをインポート
from abstract.parser import ParserBase
from funcs.plugin_loader import load_parsers
from funcs.assets import get_app_icon


class Fetcher(QThread):
    finished = Signal(list)

    def __init__(self, parser: ParserBase):
        super().__init__()
        self.parser = parser

    def run(self):
        try:
            url = self.parser.get_url()
            # サイトによってはUser-Agentがないと拒否される場合があるための配慮
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)

            res.encoding = res.apparent_encoding
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")
            results = self.parser.parse(soup)

            self.finished.emit(results)
        except Exception as e:
            print(f"Error: {e}")
            self.finished.emit([])


class NewsViewer(QMainWindow):
    __app_name__ = "newsviewer"
    __version__ = "0.0.1"
    __author__ = "Fuhito Suguri"
    __license__ = "MIT"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"ニュース・ビューアー {self.__version__}")
        self.resize(800, 500)
        self.worker = None

        # パーサーの動的ロード
        self.parsers = load_parsers()

        # ウィンドウアイコンの設定
        self.setWindowIcon(get_app_icon())

        self.toolbar = toolbar = QToolBar()
        self.addToolBar(toolbar)

        # ツールバーにコンボボックス追加
        self.combo = combo = QComboBox()
        combo.addItems(self.parsers.keys())
        combo.currentTextChanged.connect(self.fetch_news)
        toolbar.addWidget(combo)

        # UIレイアウト
        self.base = base = QWidget()
        self.setCentralWidget(base)
        self.layout = layout = QVBoxLayout(base)

        # テーブルの設定
        self.table = table = QTableWidget(0, 2)
        table.setStyleSheet("QTableWidget {font-family: monospace;}")
        table.setHorizontalHeaderLabels(["日付", "タイトル"])

        # 行番号を右寄せにする
        table.verticalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.cellDoubleClicked.connect(self.on_cell_clicked)
        self.layout.addWidget(table)

        # 列の幅調整
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # 更新ボタン
        self.btn_refresh = btn_refresh = QPushButton("ニュースを更新")
        btn_refresh.clicked.connect(self.fetch_news)
        self.layout.addWidget(btn_refresh)

        # 起動時に一度実行
        if self.parsers:
            self.fetch_news()

    def fetch_news(self):
        selected_name = self.combo.currentText()
        if not selected_name:
            return

        parser = self.parsers[selected_name]
        self.btn_refresh.setEnabled(False)

        self.worker = worker = Fetcher(parser)
        worker.finished.connect(self.display_news)
        worker.start()

    def display_news(self, news_list):
        self.table.setRowCount(0)
        for news in news_list:
            row = self.table.rowCount()
            self.table.insertRow(row)

            date_item = QTableWidgetItem(news["date"])
            title_item = QTableWidgetItem(news["title"])
            title_item.setData(Qt.ItemDataRole.UserRole, news["url"])

            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, title_item)

        self.btn_refresh.setEnabled(True)

    def on_cell_clicked(self, row, column):
        url = self.table.item(row, 1).data(Qt.ItemDataRole.UserRole)
        if url:
            webbrowser.open(url)


def main():
    app = QApplication(sys.argv)
    window = NewsViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
