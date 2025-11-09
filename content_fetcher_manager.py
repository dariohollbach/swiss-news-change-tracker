from content_fetcher import content_fetcher
from twenty_minutes_content_fetcher import twenty_minutes_content_fetcher

content_fetchers: list[content_fetcher] = [
    twenty_minutes_content_fetcher()
]
