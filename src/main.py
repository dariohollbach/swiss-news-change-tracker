from datetime import datetime
import difflib
from dateutil.parser import parse as parse_date

import database_manager
from content_fetcher_manager import content_fetchers


def main():
    """Main function to fetch articles from various sources and store them in the database."""
    for fetcher in content_fetchers:
        articles = fetcher.scrap_all_articles()
        for art in articles:
            try:
                # Parse the date and format it to 'YYYY-MM-DD HH:MM:SS' for consistency
                parsed_date = parse_date(art.publication_date)
                art.publication_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                print(
                    f"Could not parse date: {art.publication_date}, skipping article.")
                continue

            # Improve content readability by adding line breaks after sentences
            art.content = art.content.replace(". ", ". \\n")
            art.content = art.content.replace("? ", "? \\n")
            art.content = art.content.replace("! ", "! \\n")

            # Check if the news paper exists in the database, if not add it
            news_paper_id = database_manager.get_news_paper_id(
                fetcher.source_name())
            if not news_paper_id:
                news_paper_id = database_manager.add_news_paper(
                    fetcher.source_name())

            # Skip articles with empty content
            if not art.content:
                print(
                    f"{fetcher.source_name()}: Article with empty content found, skipping...")
                continue
            
            # Skip articles with empty title
            if not art.title:
                print(
                    f"{fetcher.source_name()}: Article with empty title found, skipping...")
                continue

            # Check if the article already exists in the database by title
            if db_art := database_manager.get_article_by_title(art.title):
                if db_art.content != art.content:
                    if "live" in art.content.lower() or "ticker" in art.content.lower():
                        continue  # Skip live update articles

                    # Generate a unified diff between the old and new content
                    diff = difflib.unified_diff(
                        db_art.content.split("\\n"),
                        art.content.split("\\n"),
                        fromfile='Database Content',
                        tofile='Fetched Content',
                        lineterm='\\n'
                    )

                    if '\n'.join(list(diff)) == "":
                        continue  # No changes detected

                    # Check for existing identical diffs to avoid duplicates
                    duplicated_diff = False
                    already_existing_diffs = database_manager.get_article_changes(
                        article_id=db_art.id)
                    for change in already_existing_diffs:
                        if change["change"] == '\n'.join(list(diff)):
                            duplicated_diff = True
                            break
                    if duplicated_diff:
                        continue

                    # Add the detected change to the database
                    print(
                        f"{fetcher.source_name()}: Article titled '{art.title}' published at {art.publication_date} with different content found, updating...")
                    database_manager.add_article_change(
                        db_art.id,
                        '\n'.join(list(diff)),
                        datetime.now()
                    )
                continue

            print(f"{fetcher.source_name()}: Adding article titled '{art.title}' published at {art.publication_date} to the database.")

            # Add the new article to the database
            database_manager.add_article(
                news_paper_id,
                art.title,
                art.content,
                art.publication_date
            )


if __name__ == "__main__":
    main()
