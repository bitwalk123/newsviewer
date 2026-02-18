from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

# パスを一元管理（定数として定義）
LOCAL_PARSER_DIR = Path.home() / ".local/share/newsviewer/parsers"


def get_parser_dir():
    """ローカルパーサーのディレクトリパスを返す（無ければ作成）"""
    # TODO: Windows への対応を考慮するのであれば、ロジックを変更する必要あり！
    if not LOCAL_PARSER_DIR.exists():
        LOCAL_PARSER_DIR.mkdir(parents=True, exist_ok=True)
    return LOCAL_PARSER_DIR


def open_local_parser_dir():
    """ディレクトリをシステムデフォルトのファイルブラウザで開く"""
    path = get_parser_dir()
    url = QUrl.fromLocalFile(str(path))
    QDesktopServices.openUrl(url)
