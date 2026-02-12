from abstract.parser import ParserBase
from datetime import datetime
from funcs.conv_locale import set_locale_en


class Parser(ParserBase):
    DISPLAY_NAME = "Beyond Meat (BYND)"

    def get_url(self):
        return "https://www.beyondmeat.com/en-US/newsroom/"

    def parse(self, soup):
        results = []

        # 記事全体を囲む a タグを抽出（クラス名の一部が固定と仮定）
        # ご提示の styles__Container-q5mzej-7 などを利用
        article_links = soup.find_all("a", class_=lambda x: x and 'styles__Container' in x)

        for a_tag in article_links:
            url = a_tag.get("href")
            if url and url.startswith("/"):
                url = "https://www.beyondmeat.com" + url

            # 1つの a タグの中に content ブロックが2つあるが、
            # 最初（index 0）のブロックに「日付」と「メインタイトル」が入っている
            contents = a_tag.find_all("div", class_=lambda x: x and 'styles__Content' in x)
            if not contents:
                continue

            first_content = contents[0]

            # --- タイトルの抽出 ---
            # styles__Title... クラスを持つ p タグの最初を取得
            title_tag = first_content.find("p", class_=lambda x: x and 'styles__Title' in x)
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            # --- 日付の抽出 ---
            # styles__Date... クラスを持つ p タグを取得
            # ただし、同じクラスで "press release" などのカテゴリが入っている場合があるため
            # テキストに数字（日付）が含まれているものを探す
            date_tags = first_content.find_all("p", class_=lambda x: x and 'styles__Date' in x)
            date_str = ""

            for d_tag in date_tags:
                text = d_tag.get_text(strip=True).replace('\xa0', ' ')
                # "Jan 15, 2026" のように数字が含まれている方を日付とみなす
                if any(char.isdigit() for char in text):
                    try:
                        with set_locale_en():
                            # 短縮形(Jan)とフルネーム(January)の両方に対応
                            for fmt in ("%b %d, %Y", "%B %d, %Y"):
                                try:
                                    dt = datetime.strptime(text, fmt)
                                    date_str = dt.strftime("%Y-%m-%d")
                                    break
                                except ValueError:
                                    continue
                    except:
                        date_str = text
                    break  # 日付が見つかったら終了

            results.append({
                "date": date_str,
                "title": title,
                "url": url
            })

        return results