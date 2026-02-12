from abc import ABC, abstractmethod


class ParserBase(ABC):
    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def parse(self, soup):
        """BeautifulSoupのオブジェクトを受け取り、辞書のリストを返す"""
        pass
