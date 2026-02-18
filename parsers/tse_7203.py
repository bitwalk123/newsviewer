from abstract.parser import ParserBase
import re


class Parser(ParserBase):
    """トヨタ自動車 (7203)"""
    DISPLAY_NAME = "トヨタ自動車 (7203)"

    def get_url(self) -> str:
        # 投資家情報 (IR) ページ
        return "https://global.toyota/jp/ir/"

    def parse(self, soup) -> list[dict[str, str]]:
        base_url: str = "https://global.toyota"
        results: list[dict[str, str]] = []

        # <ul class="news_contents"> 内の <li> をすべて取得
        news_list = soup.find("ul", class_="news_contents")
        if not news_list:
            return []

        items = news_list.find_all("li")
        for item in items:
            # --- 日付の抽出と変換 ---
            # <span>2026/02/06</span> を取得
            date_tag = item.find("span")
            date_text = date_tag.get_text(strip=True) if date_tag else ""

            formatted_date = date_text
            # "2026/02/06" 形式から "/" を "-" に置換、
            # もし形式が違っても対応できるよう数字を抽出して整形
            date_parts = re.findall(r'\d+', date_text)
            if len(date_parts) == 3:
                year = date_parts[0]
                month = date_parts[1].zfill(2)
                day = date_parts[2].zfill(2)
                formatted_date = f"{year}-{month}-{day}"

            # --- タイトルとリンクの抽出 ---
            a_tag = item.find("a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            href = a_tag.get("href")

            # 相対パスを絶対URLに変換
            if href.startswith("/"):
                full_url = base_url + href
            else:
                full_url = href

            results.append({
                "date": formatted_date,
                "title": title,
                "url": full_url
            })

        return results
