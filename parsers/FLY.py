from abstract.parser import ParserBase
from datetime import datetime

from funcs.conv_locale import set_locale_en


class Parser(ParserBase):
    DISPLAY_NAME = "Firefly Aerospace (FLY)"

    def get_url(self):
        return "https://fireflyspace.com/news/"

    def parse(self, soup):
        results = []
        articles = soup.find_all("div", class_="article__content")

        for article in articles:
            h2_tag = article.find("h2")
            if not h2_tag: continue
            a_tag = h2_tag.find("a")
            if not a_tag: continue

            title = a_tag.get_text(strip=True)
            url = a_tag.get("href")

            time_tag = article.find("time")
            date_str = ""
            if time_tag:
                # 特殊な空白文字 (\xa0 など) を通常の半角スペースに置換し、前後の余白を消す
                raw_date = time_tag.get_text().replace('\xa0', ' ').strip()

                try:
                    # 英語の月名を正しく解釈するためにロケールを一時変更
                    with set_locale_en():
                        dt = datetime.strptime(raw_date, "%B %d, %Y")
                        date_str = dt.strftime("%Y-%m-%d")
                except Exception as e:
                    # デバッグ用にエラーが出た文字列をそのまま出す
                    print(f"DEBUG: Parse failed for '{raw_date}' - {e}")
                    date_str = raw_date

            results.append({
                "date": date_str,
                "title": title,
                "url": url
            })

        return results