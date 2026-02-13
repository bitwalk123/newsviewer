import importlib
import pkgutil

import parsers
from abstract.parser import ParserBase


def load_parsers():
    """parsersディレクトリからパーサーを動的に読み込む"""
    found_parsers = {}

    # parsersパッケージのパス内にあるモジュールを走査
    for loader, module_name, is_pkg in pkgutil.iter_modules(parsers.__path__):
        full_module_name = f"parsers.{module_name}"
        # 動的インポート
        try:
            module = importlib.import_module(full_module_name)
            # 再読み込みが必要な場合（開発中など）に対応
            importlib.reload(module)

            # モジュール内のクラスを走査
            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                # ParserBaseを継承し、かつParserBase自身ではない具象クラスを探す
                if (isinstance(attr, type) and
                        issubclass(attr, ParserBase) and
                        attr is not ParserBase):
                    # パーサー側で定義した DISPLAY_NAME をキーにする
                    # 定義がない場合はモジュール名をフォールバックにする
                    display_name = getattr(attr, "DISPLAY_NAME", module_name)
                    found_parsers[display_name] = attr()
        except Exception as e:
            print(f"Failed to load parser {full_module_name}: {e}")

    return found_parsers
