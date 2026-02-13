from abstract.parser import ParserBase
from datetime import datetime
from funcs.conv_locale import set_locale_en


class Parser(ParserBase):
    """NVIDIA (NVDA)"""
    DISPLAY_NAME = "NVIDIA (NVDA)"

    def get_url(self):
        # ニュースルームのトップ（最新ニュース）
        return "https://nvidianews.nvidia.com/"

    def parse(self, soup):
        results = []

        # ニュース項目を保持する <article class="tiles-item"> をすべて取得
        articles = soup.find_all("article", class_=lambda x: x and 'tiles-item' in x)

        for article in articles:
            # --- タイトルとリンクの抽出 ---
            # <h3 class="tiles-item-text-title"> 内の <a> タグを探す
            title_container = article.find("h3", class_="tiles-item-text-title")
            if not title_container:
                continue

            a_tag = title_container.find("a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            url = a_tag.get("href")

            # --- 日付の抽出と変換 ---
            # <div class="tiles-item-text-date"> を探す
            date_tag = article.find("div", class_="tiles-item-text-date")
            date_str = ""

            if date_tag:
                raw_date = date_tag.get_text(strip=True).replace('\xa0', ' ')
                try:
                    # 英語ロケールを使用して "February 12, 2026" 形式をパース
                    with set_locale_en():
                        dt = datetime.strptime(raw_date, "%B %d, %Y")
                        date_str = dt.strftime("%Y-%m-%d")
                except Exception:
                    # パース失敗時は元の文字列を保持
                    date_str = raw_date

            results.append({
                "date": date_str,
                "title": title,
                "url": url
            })

        return results