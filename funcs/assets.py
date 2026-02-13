import os
from pathlib import Path

from PySide6.QtGui import QIcon


def get_app_icon() -> QIcon:
    """
    RPMパッケージ化を考慮したアイコン取得関数
    1. システム標準パス (/usr/share/icons/...)
    2. 開発環境の相対パス (resources/icons/...)
    3. フォールバック (空のアイコン)
    """
    icon_name = "newsviewer.svg"

    # 1. システム標準の場所 (RPMインストール後の期待値)
    # Fedoraの標準的なアイコンパス
    system_icon_path = Path("/usr/share/icons/hicolor/scalable/apps") / icon_name
    if system_icon_path.exists():
        return QIcon(str(system_icon_path))

    # 2. 開発環境の相対パス
    # 実行中のスクリプト(main.py)からの相対位置
    base_dir = Path(__file__).resolve().parent
    local_icon_path = os.path.join(base_dir, "resources", "icons", icon_name)
    if os.path.exists(local_icon_path):
        return QIcon(str(local_icon_path))

    # 3. フォールバック
    # アイコンが見つからない場合、実行時にエラーにせず、標準アイコンを返す
    return QIcon.fromTheme("text-x-generic")  # 汎用的な書類アイコンなど
