from abstract.parser import ParserBase


class Parser4689(ParserBase):
    """LINEヤフー (4689)"""

    def get_url(self):
        return "https://www.lycorp.co.jp/ja/news/"

    def parse(self, soup):
        items = soup.find_all("li", class_="c-col")
        results = []
        for item in items:
            a_tag = item.find("a", class_="c-article-panel-d2")
            if a_tag:
                results.append({
                    "url": a_tag.get("href"),
                    "date": item.find("time").get_text(strip=True),
                    "title": item.find("p").get_text(strip=True)
                })
        return results
