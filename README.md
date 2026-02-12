# newsviewer

特定の銘柄（東証・米国株）のIRサイトやニュースルームから最新情報を自動取得し、デスクトップ上で素早く確認・閲覧するためのGUIアプリケーションです。

## 主な機能
- **マルチスレッドによる非同期取得**: `QThread` を利用することで、ニュース取得中もGUIの操作性を損なわない設計としています。
- **プラグイン可能なパースロジック**: `ParserBase` 抽象クラスを継承することで、各企業のサイトごとに異なるHTML構造を柔軟に解析可能です。
- **日付フォーマットの統一**: サイトごとに異なる日付表記（日本株の「年月日」や米国株の英語表記）を `YYYY-MM-DD` 形式に自動整形し、時系列での視認性を高めています。
- **ダブルクリックでの詳細閲覧**: テーブル上の項目をダブルクリックすることで、標準ブラウザから即座にソース元（IR記事等）を開くことができます。

## 技術スタック
- **Language**: Python 3.x
- **GUI Framework**: PySide6 (Qt for Python)
- **HTTP Library**: requests (User-Agent制御、タイムアウト設定済)
- **Scraping**: BeautifulSoup4
- **Architecture**: OOP (抽象クラスによるポリモーフィズムの活用), マルチスレッド

## プログラム構成（主要クラス）
- `ParserBase`: すべての銘柄パーサーの基底となる抽象クラス。
- `tse_4005.py FLY.py など`: 銘柄パーサーの実装例。
- `Fetcher`: ネットワーク通信とパース処理を担当するワーカースレッド。
- `NewsViewer`: メインウィンドウおよびUI制御ロジック。
---

## 免責事項 / Disclaimer

### 日本語

本プログラムおよびそのソースコードは、技術情報の共有および学習を目的としたものです。本プログラムを利用してウェブサイトのスクレイピング（自動データ収集）を行う際は、以下の点に十分注意してください。

* **利用規約の遵守**: 対象サイトの利用規約および `robots.txt` を必ず確認し、その指示に従ってください。
* **サーバー負荷への配慮**: 相手サーバーに過度な負荷をかけないよう、適切な待機時間（スリープ）を設けて実行してください。
* **自己責任**: 本プログラムの利用によって生じた、いかなるトラブル、損失、損害（アカウントの停止や法的措置等を含む）についても、作者は一切の責任を負いません。すべて利用者自身の責任において使用してください。

---

### English

This program and its source code are provided for technical information sharing and educational purposes only. When using this program for web scraping (automated data collection), please adhere to the following guidelines:

* **Compliance with Terms of Service**: Always check the target website's Terms of Use and its `robots.txt` file, and ensure you operate within their guidelines.
* **Server Etiquette**: Ensure appropriate delay (sleep) between requests to avoid imposing an excessive load on the target server.
* **Use at Your Own Risk**: The author shall not be held responsible for any issues, losses, or damages (including account suspension or legal action) resulting from the use of this program. Users assume all responsibility for their actions.

---
