from content_fetcher import scrap_all_articles
import database_manager


def main():
    articles = scrap_all_articles()
    for art in articles:
        news_paper_id = database_manager.get_news_paper_id('20 Minuten')
        if not news_paper_id:
            news_paper_id = database_manager.add_news_paper('20 Minuten')
            
        if not art.content:
            print("Article with empty content found, skipping...")
            continue
        
        if not art.title:
            print("Article with empty title found, skipping...")
            continue

        database_manager.add_article(
            news_paper_id,
            art.title,
            art.content,
            "2024-01-01"  # Placeholder date; in a real scenario, extract the actual publication date
        )
        
if __name__ == "__main__":
    main()
