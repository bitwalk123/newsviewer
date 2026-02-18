from abc import ABC, abstractmethod


class ParserBase(ABC):
    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def parse(self, soup) -> list[dict[str, str]]:
        """BeautifulSoupのオブジェクトを受け取り、辞書のリストを返す"""
        pass
