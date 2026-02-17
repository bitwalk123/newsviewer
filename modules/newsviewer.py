import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from abstract.parser import ParserBase
from funcs.assets import get_app_icon
from funcs.plugin_loader import load_parsers
from funcs.utils import open_local_parser_dir
from modules.fetcher import Fetcher
from widgets.buttons import ActionFolder, Button
from widgets.combos import ComboBox
from widgets.containers import MainWindow, PadH, Widget
from widgets.layouts import VBoxLayout
from widgets.tables import TableWidget
from widgets.toolbars import ToolBar


class NewsViewer(MainWindow):
    __app_name__ = "newsviewer"
    __version__ = "0.0.3"
    __author__ = "Fuhito Suguri"
    __license__ = "MIT"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"ニュース・ビューアー {self.__version__}")
        self.resize(800, 500)
        self.worker: Fetcher | None = None

        # パーサーの動的ロード
        self.parsers: dict[str, ParserBase] = load_parsers()

        # ウィンドウアイコンの設定
        self.setWindowIcon(get_app_icon())

        toolbar = ToolBar()
        self.addToolBar(toolbar)

        # ツールバーにコンボボックス追加
        self.combo = combo = ComboBox()
        combo.addItems(list(self.parsers.keys()))
        combo.currentTextChanged.connect(self.fetch_news)
        toolbar.addWidget(combo)

        pad = PadH()
        toolbar.addWidget(pad)

        # Open
        action_open = ActionFolder(self)
        action_open.triggered.connect(open_local_parser_dir)
        toolbar.addAction(action_open)

        # UIレイアウト
        base = Widget()
        self.setCentralWidget(base)

        layout = VBoxLayout()
        base.setLayout(layout)

        # テーブルの設定
        self.table = table = TableWidget(0, 2)
        table.cellDoubleClicked.connect(self.on_cell_clicked)
        layout.addWidget(table)

        # 更新ボタン
        self.btn_refresh = btn_refresh = Button("ニュースを更新")
        btn_refresh.clicked.connect(self.fetch_news)
        layout.addWidget(btn_refresh)

        # 起動時に一度実行
        if self.parsers:
            self.fetch_news()

    def fetch_news(self) -> None:
        selected_name = self.combo.currentText()
        if not selected_name:
            return

        parser = self.parsers[selected_name]
        self.btn_refresh.setEnabled(False)

        self.worker = worker = Fetcher(parser)
        worker.finished.connect(self.display_news)
        worker.start()

    def display_news(self, news_list) -> None:
        self.table.setNews(news_list)
        self.btn_refresh.setEnabled(True)

    def on_cell_clicked(self, row: int, column: int) -> None:
        item: QTableWidgetItem | None = self.table.item(row, 1)
        if item:
            url: str | None = item.data(Qt.ItemDataRole.UserRole)
            if url:
                webbrowser.open(url)
