import sys
import webbrowser
from typing import Dict

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

from abstract.parser import ParserBase
from parsers.parser4005 import Parser4005
from parsers.parser4689 import Parser4689


class Fetcher(QThread):
    finished = Signal(list)

    def __init__(self, parser: ParserBase):
        super().__init__()
        self.parser = parser

    def run(self):
        try:
            url = self.parser.get_url()
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)

            res.encoding = res.apparent_encoding
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")
            # 渡されたパーサーに解析を丸投げ
            results = self.parser.parse(soup)

            self.finished.emit(results)
        except Exception as e:
            print(f"Error: {e}")
            self.finished.emit([])


class NewsViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ニュース・ビューアー")
        self.resize(800, 600)
        self.worker = None

        self.parsers: Dict[str, ParserBase] = {
            "住友化学 (4005)": Parser4005(),
            "LINEヤフー (4689)": Parser4689(),
        }

        # ツールバー
        self.toolbar = toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 銘柄選択用コンボボックス
        self.combo = combo = QComboBox()
        combo.addItems(self.parsers.keys())
        combo.currentTextChanged.connect(self.fetch_news)
        toolbar.addWidget(combo)

        # レイアウト
        self.base = base = QWidget()
        self.setCentralWidget(base)
        self.layout = layout = QVBoxLayout(base)

        # テーブルの設定
        self.table = table = QTableWidget(0, 2)
        table.setStyleSheet("QTableWidget {font-family: monospace;}")
        table.setHorizontalHeaderLabels(["日付", "タイトル"])
        # 行ヘッダー（垂直ヘッダー）を取得して、右寄せ＋垂直中央に設定
        table.verticalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )  # 行選択
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )  # 編集禁止
        table.cellDoubleClicked.connect(self.on_cell_clicked)  # クリックイベント
        self.layout.addWidget(table)

        # 列の幅調整
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # 日付は内容に合わせる
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # タイトルは伸ばす

        # 更新ボタン
        self.btn_refresh = btn_refresh = QPushButton("ニュースを更新")
        btn_refresh.clicked.connect(self.fetch_news)
        self.layout.addWidget(btn_refresh)

        # 起動時に一度実行
        self.fetch_news()

    def fetch_news(self):
        # 選択されている銘柄名を取得
        selected_name = self.combo.currentText()
        # 対応するパーサーを取り出す
        parser = self.parsers[selected_name]
        # スレッドにそのパーサーを託す
        self.worker = worker = Fetcher(parser)
        worker.finished.connect(self.display_news)
        worker.start()

    def display_news(self, news_list):
        self.table.setRowCount(0)
        for news in news_list:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # 日付アイテム
            date_item = QTableWidgetItem(news["date"])
            # タイトルアイテム（URLをデータとして持たせる）
            title_item = QTableWidgetItem(news["title"])
            title_item.setData(Qt.ItemDataRole.UserRole, news["url"])

            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, title_item)

        self.btn_refresh.setEnabled(True)

    def on_cell_clicked(self, row, column):
        # どの列をクリックしてもタイトル列(1)に保存したURLを取得
        url = self.table.item(row, 1).data(Qt.ItemDataRole.UserRole)
        if url:
            webbrowser.open(url)


def main():
    app = QApplication(sys.argv)
    win = NewsViewer()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
