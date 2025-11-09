from datetime import datetime
import difflib

import database_manager
from content_fetcher import scrap_all_articles


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

        if db_art := database_manager.get_article_by_title(art.title):
            if db_art.content != art.content:
                if "live" in art.content:
                    continue  # Skip live update articles
                print(f"Article titled '{art.title}' with different content found, updating...")
                diff = difflib.unified_diff(
                    db_art.content.splitlines(),
                    art.content.splitlines(),
                    fromfile='Database Content',
                    tofile='Fetched Content',
                    lineterm=''
                )
                database_manager.add_article_change(
                    db_art.id,
                    '\n'.join(list(diff)),
                    datetime.now(datetime.timezone.utc)
                    )
                print('\n'.join(list(diff)))
            continue

        print(f"Adding article titled '{art.title}' to the database.")

        database_manager.add_article(
            news_paper_id,
            art.title,
            art.content
        )
        
if __name__ == "__main__":
    main()
