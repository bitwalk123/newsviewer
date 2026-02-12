import locale
from contextlib import contextmanager


@contextmanager
def set_locale_en():
    """一時的にロケールを英語(US)に変更するコンテキストマネージャ"""
    current_locale = locale.getlocale(locale.LC_TIME)
    try:
        # Windows/Linux両方に対応するための指定
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'en_US')  # Windows等の環境用
        yield
    finally:
        locale.setlocale(locale.LC_TIME, current_locale)
