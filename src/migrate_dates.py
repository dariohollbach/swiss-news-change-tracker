import sqlite3
from email.utils import parsedate_to_datetime

def migrate_publication_dates():
    db_path = "swiss_news_articles.db"
    print(f"Connecting to database at '{db_path}'...")
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    try:
        print("Fetching all articles...")
        cursor.execute("SELECT id, publication_date FROM articles")
        articles = cursor.fetchall()
        print(f"Found {len(articles)} articles to check.")

        for article_id, old_date_str in articles:
            try:
                parsed_date = parsedate_to_datetime(old_date_str)
                new_date_str = parsed_date.strftime('%Y-%m-%d %H:%M:%S')

                if new_date_str != old_date_str:
                    print(f"Updating article {article_id}: '{old_date_str}' -> '{new_date_str}'")
                    cursor.execute("UPDATE articles SET publication_date = ? WHERE id = ?", (new_date_str, article_id))
            except (TypeError, ValueError):
                print(f"Skipping article {article_id}: Could not parse date '{old_date_str}'. It might be in the correct format already.")

        db_connection.commit()
        print("Database update complete and changes committed.")
    finally:
        db_connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    confirmation = input("This script will modify the 'publication_date' for existing articles. Enter Y to continue...")
    if confirmation.upper() == "Y":
        migrate_publication_dates()