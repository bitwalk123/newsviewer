import requests
from PySide6.QtCore import QThread, Signal
from bs4 import BeautifulSoup

from abstract.parser import ParserBase


class Fetcher(QThread):
    finished = Signal(list)

    def __init__(self, parser: ParserBase) -> None:
        super().__init__()
        self.parser: ParserBase = parser

    def run(self) -> None:
        try:
            url: str = self.parser.get_url()
            # サイトによってはUser-Agentがないと拒否される場合があるための配慮
            headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)

            res.encoding = res.apparent_encoding
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")
            results: list[dict[str, str]] = self.parser.parse(soup)

            self.finished.emit(results)
        except Exception as e:
            print(f"Error: {e}")
            self.finished.emit([])
