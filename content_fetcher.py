import feedparser
import requests
from bs4 import BeautifulSoup
import article

def scrap_all_articles() -> list[article.Article]:
    d = feedparser.parse('https://partner-feeds.beta.20min.ch/rss/20minuten')
    articles = []

    for entry in d.entries:
        content = get_text_content(entry.link)
        articles.append(article.Article(title=entry.title, content=content))

    return articles

def get_text_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    if not article:
        return ""
    elements = article.find_all(['h2', 'p'])

    content = '\n\n'.join(el.get_text() for el in elements)
    return content
