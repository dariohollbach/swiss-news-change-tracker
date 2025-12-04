from content_fetcher import content_fetcher
from twenty_minutes_content_fetcher import twenty_minutes_content_fetcher
from watson_content_fetcher import watson_content_fetcher
from srf_ch_content_fetcher import srf_ch_content_fetcher

"""Manages a list of content fetchers for different news sources."""
content_fetchers: list[content_fetcher] = [
    twenty_minutes_content_fetcher(),
    watson_content_fetcher(),
    srf_ch_content_fetcher(),
]
