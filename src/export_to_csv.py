import sqlite3
import csv
import os

def export_articles_and_changes_to_csv(db_path, output_csv_path, start_date, end_date):
    """Exports articles and their changes within a date range to a CSV file."""
    print(f"Connecting to database at '{db_path}'...")
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    query = """
    SELECT
        np.name AS newspaper_name,
        a.title AS article_title,
        a.publication_date,
        ac.id AS change_id,
        ac.change AS change_content,
        ac.change_timestamp,
        ac.classification
    FROM
        articles a
    JOIN
        NEWS_PAPERS np ON a.news_paper_id = np.id
    LEFT JOIN
        article_changes ac ON a.id = ac.article_id
    WHERE
        DATE(a.publication_date) BETWEEN ? AND ?
    ORDER BY
        np.name, a.publication_date, ac.change_timestamp;
    """

    try:
        print(f"Fetching data for articles published between {start_date} and {end_date}...")
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found for the specified date range.")
            return

        header = [description[0] for description in cursor.description]

        print(f"Writing {len(rows)} rows to '{output_csv_path}'...")
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(rows)
        
        print("Export complete.")

    finally:
        db_connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    DB_FILE = 'swiss_news_articles.db'
    OUTPUT_FILE = 'article_changes_export.csv'
    
    START_DATE = "2025-11-10"
    END_DATE = "2025-11-20"

    export_articles_and_changes_to_csv(DB_FILE, OUTPUT_FILE, START_DATE, END_DATE)