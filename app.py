import sys

from PySide6.QtWidgets import QApplication

# 基底クラスとパッケージをインポート
from modules.newsviewer import NewsViewer


def main() -> None:
    app = QApplication(sys.argv)
    window = NewsViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
