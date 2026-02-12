from abstract.parser import ParserBase
from datetime import datetime
import re


class Parser(ParserBase):
    """住友化学 (4005)"""
    DISPLAY_NAME = "住友化学 (4005)"

    def get_url(self):
        return "https://www.sumitomo-chem.co.jp/news/"

    def parse(self, soup):
        base_url = "https://www.sumitomo-chem.co.jp"
        # <ul class="m-list-news"> 内の <li> を探す
        news_list = soup.find("ul", class_="m-list-news")
        if not news_list:
            return []

        items = news_list.find_all("li")
        results = []
        for item in items:
            a_tag = item.find("a")
            if not a_tag:
                continue

            # 相対パスを絶対URLに変換
            relative_url = a_tag.get("href")
            full_url = base_url + relative_url if relative_url.startswith("/") else relative_url

            # 日付の取得と YYYY-MM-DD への変換
            date_el = item.find("p", class_="news-date")
            date_text = date_el.get_text(strip=True) if date_el else ""

            formatted_date = date_text
            # 数字の塊をリストで取得 (例: "2026年02月05日" -> ["2026", "02", "05"])
            date_parts = re.findall(r'\d+', date_text)
            if len(date_parts) == 3:
                year = date_parts[0]
                month = date_parts[1].zfill(2)
                day = date_parts[2].zfill(2)
                formatted_date = f"{year}-{month}-{day}"

            # タイトルの取得
            title_el = item.find("p", class_="news-ttl")
            title_text = title_el.get_text(strip=True) if title_el else ""

            results.append({
                "url": full_url,
                "date": formatted_date,
                "title": title_text
            })
        return results