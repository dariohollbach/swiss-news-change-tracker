import sqlite3

def add_classification_column():
    """Adds a 'classification' column to the 'article_changes' table."""
    db_path = "swiss_news_articles.db"
    print(f"Connecting to database at '{db_path}'...")
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    try:
        # Check if the column already exists to make the script safe to run multiple times
        cursor.execute("PRAGMA table_info(article_changes)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'classification' in columns:
            print("Column 'classification' already exists in 'article_changes' table. No migration needed.")
            return

        print("Adding 'classification' column to 'article_changes' table...")
        
        alter_query = """
        ALTER TABLE article_changes
        ADD COLUMN classification TEXT NOT NULL DEFAULT 'not classified'
        CHECK(classification IN ('not classified', 'typo', 'content change'))
        """
        cursor.execute(alter_query)
        
        db_connection.commit()
        print("Database schema updated successfully. Data has been preserved.")

    finally:
        db_connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    add_classification_column()