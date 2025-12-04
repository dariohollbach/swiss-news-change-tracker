import feedparser
import requests
from bs4 import BeautifulSoup
import article
from content_fetcher import content_fetcher

class twenty_minutes_content_fetcher(content_fetcher):
    def scrap_all_articles(self) -> list[article.Article]:
        d = feedparser.parse('https://partner-feeds.beta.20min.ch/rss/20minuten')
        articles = []

        for entry in d.entries:
            if  "title" not in entry.keys() or "published" not in entry.keys():
                continue
            if not entry.title or not entry.link or not entry.published:
                continue
            content = self.get_text_content(entry.link)
            articles.append(article.Article(title=entry.title, content=content, publication_date=entry.published))

        return articles
    
    def source_name(self) -> str:
        return "20 Minuten"

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

