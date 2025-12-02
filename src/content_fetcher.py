import article

from abc import ABC, abstractmethod

class content_fetcher(ABC):
    @abstractmethod
    def scrap_all_articles(self) -> list[article.Article]:
        pass
    
    @abstractmethod
    def source_name(self) -> str:
        pass