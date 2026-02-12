from abstract.parser import ParserBase
from datetime import datetime
import re


class Parser(ParserBase):
    """LINEヤフー (4689)"""
    DISPLAY_NAME = "LINEヤフー (4689)"

    def get_url(self):
        return "https://www.lycorp.co.jp/ja/news/"

    def parse(self, soup):
        # 記事リストの <li> を取得
        items = soup.find_all("li", class_="c-col")
        results = []
        for item in items:
            # 記事へのリンク A タグを取得
            a_tag = item.find("a", class_="c-article-panel-d2")
            if a_tag:
                # 日付の取得と YYYY-MM-DD への変換
                time_tag = item.find("time")
                raw_date = time_tag.get_text(strip=True) if time_tag else ""

                formatted_date = raw_date
                # 数字の塊をリストで取得 (例: "2026年2月5日" -> ["2026", "2", "5"])
                date_parts = re.findall(r'\d+', raw_date)
                if len(date_parts) == 3:
                    year = date_parts[0]
                    month = date_parts[1].zfill(2)  # 1桁なら 01 に補完
                    day = date_parts[2].zfill(2)  # 1桁なら 05 に補完
                    formatted_date = f"{year}-{month}-{day}"

                # タイトル（pタグ）の取得
                title_tag = item.find("p")
                title_text = title_tag.get_text(strip=True) if title_tag else ""

                results.append({
                    "url": a_tag.get("href"),
                    "date": formatted_date,
                    "title": title_text
                })
        return results