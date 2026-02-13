import sys
import pkgutil
import importlib
from pathlib import Path

# 1. パッケージとしての parsers をインポート
import parsers

# 2. 基底クラスも必要
from abstract.parser import ParserBase


def load_parsers():
    """システム側とユーザーローカルの両方からパーサーを動的に読み込む"""
    found_parsers = {}

    # 1. システム側のパス（パッケージとして扱う）
    system_paths = list(parsers.__path__)
    for loader, module_name, is_pkg in pkgutil.iter_modules(system_paths):
        full_module_name = f"parsers.{module_name}"
        _add_parser_to_dict(full_module_name, module_name, found_parsers)

    # 2. ユーザーローカルのパス（単独モジュールとして扱う）
    local_parser_dir = Path.home() / ".local/share/newsviewer/parsers"
    if local_parser_dir.exists():
        local_path_str = str(local_parser_dir)
        if local_path_str not in sys.path:
            sys.path.insert(0, local_path_str)

        # ローカルディレクトリ内を直接走査
        for loader, module_name, is_pkg in pkgutil.iter_modules([local_path_str]):
            # ローカルは 'parsers.' を付けずに直接インポート
            _add_parser_to_dict(module_name, module_name, found_parsers)

    return found_parsers


def _add_parser_to_dict(full_module_name, short_name, found_parsers):
    """モジュールをインポートしてクラスを辞書に追加する補助関数"""
    try:
        module = importlib.import_module(full_module_name)
        importlib.reload(module)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and
                    issubclass(attr, ParserBase) and
                    attr is not ParserBase):
                display_name = getattr(attr, "DISPLAY_NAME", short_name)
                found_parsers[display_name] = attr()
    except Exception as e:
        print(f"Failed to load parser {full_module_name}: {e}")