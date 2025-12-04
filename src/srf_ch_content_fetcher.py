import feedparser
import requests
from bs4 import BeautifulSoup
import article
from content_fetcher import content_fetcher

RSS_FEED_URL = 'https://www.srf.ch/news/bnf/rss/1646'

class srf_ch_content_fetcher(content_fetcher):
    def scrap_all_articles(self) -> list[article.Article]:
        d = feedparser.parse(RSS_FEED_URL)
        articles = []

        for entry in d.entries:
            if  "title" not in entry.keys() or "published" not in entry.keys():
                continue
            if not entry.title or not entry.link:
                continue
            content = self.get_text_content(entry.link)
            articles.append(article.Article(title=entry.title, content=content, publication_date=entry.published))

        return articles
    
    def source_name(self) -> str:
        return "SRF News"

    def get_text_content(self, url: str) -> str:
        """Fetches and extracts the main text content from a given article URL."""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.find('article')
        if not article:
            return ""
        elements = article.find_all(['p'])

        content = '\n\n'.join(el.get_text() for el in elements)
        return content

