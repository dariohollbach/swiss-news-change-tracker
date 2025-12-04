import sqlite3
from typing import Optional

import article
from news_paper import NewsPaper


# Database initialization
def create_database():
    """Creates the SQLite database with the required tables."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("DROP TABLE IF EXISTS NEWS_PAPERS")
    cursor.execute("""
    CREATE TABLE NEWS_PAPERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )""")

    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("""
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_paper_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        publication_date TEXT NOT NULL,
        FOREIGN KEY(news_paper_id) REFERENCES NEWS_PAPERS(id) ON DELETE CASCADE
    )""")

    cursor.execute("DROP TABLE IF EXISTS article_changes")
    cursor.execute("""
    CREATE TABLE article_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL,
        change TEXT NOT NULL,
        change_timestamp TEXT NOT NULL,
        classification TEXT NOT NULL DEFAULT 'not classified' CHECK(classification IN ('not classified', 'typo', 'content change')),
        FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
    )""")

    db_connection.commit()
    db_connection.close()


# News Paper Management
def add_news_paper(name: str) -> int:
    """Adds a news paper to the database and returns its ID."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("INSERT INTO NEWS_PAPERS (name) VALUES (?)", (name,))
    news_paper_id = cursor.lastrowid

    db_connection.commit()
    db_connection.close()

    return news_paper_id


def get_news_paper_id(name: str) -> Optional[int]:
    """Retrieves the ID of a news paper by its name."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("SELECT id FROM NEWS_PAPERS WHERE name = ?", (name,))
    result = cursor.fetchone()

    db_connection.close()

    if result:
        return result[0]
    return None


def get_all_news_papers() -> list[NewsPaper]:
    """Retrieves all news papers from the database."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("SELECT name, id FROM NEWS_PAPERS")
    results = cursor.fetchall()

    db_connection.close()

    return [NewsPaper(title=row[0], id=row[1]) for row in results]


# Article Management
def add_article(news_paper_id: int, title: str, content: str, publication_date: str) -> int:
    """Adds an article to the database and returns its ID."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO articles (news_paper_id, title, content, publication_date)
    VALUES (?, ?, ?, ?)
    """, (news_paper_id, title, content, publication_date))

    article_id = cursor.lastrowid

    db_connection.commit()
    db_connection.close()

    return article_id


def get_article_by_title(title: str) -> Optional[article.Article]:
    """Retrieves an article by its title."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
    result = cursor.fetchone()

    db_connection.close()

    if result:
        return article.Article(
            id=result[0],
            title=result[2],
            content=result[3],
            publication_date=result[4]
        )
    return None


def get_article_by_id(article_id: int) -> Optional[article.Article]:
    """Retrieves an article by its ID."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    result = cursor.fetchone()

    db_connection.close()

    if result:
        return article.Article(
            id=result[0],
            title=result[2],
            content=result[3],
            publication_date=result[4]
        )
    return None


def delete_article(article_id: int):
    """Deletes an article by its ID."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))

    db_connection.commit()
    db_connection.close()


def get_all_articles_of_news_paper(news_paper_id: int, limit: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[article.Article]:
    """Retrieves all articles of a specific news paper, with optional filtering by date range and limit."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    query = "SELECT * FROM articles WHERE news_paper_id = ?"
    params = (news_paper_id,)
    if start_date:
        query += " AND strftime('%Y-%m-%d', publication_date) >= ?"
        params += (start_date,)
    if end_date:
        query += " AND strftime('%Y-%m-%d', publication_date) <= ?"
        params += (end_date,)

    query += " ORDER BY publication_date DESC"
    if limit:
        query += " LIMIT ?"
        params += (limit,)
    cursor.execute(query, params)
    results = cursor.fetchall()

    db_connection.close()

    articles = []
    for row in results:
        articles.append(article.Article(
            id=row[0],
            title=row[2],
            content=row[3],
            publication_date=row[4]
        ))
    return articles


# Article Change Management
def add_article_change(article_id: int, change: str, change_timestamp: str) -> int:
    """Adds a change record for an article and returns the change ID."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute("""
    INSERT INTO article_changes (article_id, change, change_timestamp)
    VALUES (?, ?, ?)
    """, (article_id, change, change_timestamp))

    change_id = cursor.lastrowid

    db_connection.commit()
    db_connection.close()

    return change_id


def get_article_changes(article_id: int) -> list[dict]:
    """Retrieves all changes for a specific article."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT id, change, change_timestamp, classification FROM article_changes WHERE article_id = ?", (article_id,))
    results = cursor.fetchall()

    db_connection.close()

    changes = []
    for row in results:
        changes.append({
            "id": row[0],
            "change": row[1],
            "change_timestamp": row[2],
            "classification": row[3]
        })
    return changes


def update_change_classification(change_id: int, classification: str):
    """Updates the classification of a specific article change."""
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()

    cursor.execute(
        "UPDATE article_changes SET classification = ? WHERE id = ?",
        (classification, change_id)
    )

    db_connection.commit()
    db_connection.close()


if __name__ == "__main__":
    """Utility to create or reset the database."""
    confirmation = input(
        "This will delete the existing database and create a new one. Enter Y to continue...")
    if confirmation.upper() == "Y":
        create_database()
