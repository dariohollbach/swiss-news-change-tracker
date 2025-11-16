from datetime import datetime
import difflib

import database_manager
from content_fetcher_manager import content_fetchers


def main():
    for fetcher in content_fetchers:
        articles = fetcher.scrap_all_articles()
        for art in articles:
            art.content = art.content.replace(". ", ". \\n")
            art.content = art.content.replace("? ", "? \\n")
            art.content = art.content.replace("! ", "! \\n")
            
            news_paper_id = database_manager.get_news_paper_id(fetcher.source_name())
            if not news_paper_id:
                news_paper_id = database_manager.add_news_paper(fetcher.source_name())
                
            if not art.content:
                print(f"{fetcher.source_name()}: Article with empty content found, skipping...")
                continue
            
            if not art.title:
                print(f"{fetcher.source_name()}: Article with empty title found, skipping...")
                continue

            if db_art := database_manager.get_article_by_title(art.title):
                if db_art.content != art.content:
                    if "live" in art.content.lower():
                        continue  # Skip live update articles
                    
                    print(f"{fetcher.source_name()}: Article titled '{art.title}' published at {art.publication_date} with different content found, updating...")
                    diff = difflib.unified_diff(
                        db_art.content.split("\\n"),
                        art.content.split("\\n"),
                        fromfile='Database Content',
                        tofile='Fetched Content',
                        lineterm='\\n'
                    )
                    already_existing_diffs = database_manager.get_article_changes(article_id=db_art.id)
                    for change in already_existing_diffs:
                        if change["change"] == '\n'.join(list(diff)):
                            continue
                        break
                
                    database_manager.add_article_change(
                        db_art.id,
                        '\n'.join(list(diff)),
                        datetime.now()
                        )
                    print('\n'.join(list(diff)))
                continue

            print(f"{fetcher.source_name()}: Adding article titled '{art.title}' published at {art.publication_date} to the database.")

            database_manager.add_article(
                news_paper_id,
                art.title,
                art.content,
                art.publication_date
            )
        
if __name__ == "__main__":
    main()
