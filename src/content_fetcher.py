import article

from abc import ABC, abstractmethod

class content_fetcher(ABC):
    """Abstract base class for content fetchers."""
    @abstractmethod
    def scrap_all_articles(self) -> list[article.Article]:
        """Scrape all articles from the source."""
        pass
    
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the content source."""
        pass