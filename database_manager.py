import sqlite3
from typing import Optional

def create_database():
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
        UNIQUE(title, publication_date),
        FOREIGN KEY(news_paper_id) REFERENCES NEWS_PAPERS(id) ON DELETE CASCADE
    )""")
    
    db_connection.commit()
    db_connection.close()
    
if __name__ == "__main__":
    create_database()
    
def add_news_paper(name: str) -> int:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("INSERT INTO NEWS_PAPERS (name) VALUES (?)", (name,))
    news_paper_id = cursor.lastrowid
    
    db_connection.commit()
    db_connection.close()
    
    return news_paper_id

def get_news_paper_id(name: str) -> Optional[int]:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT id FROM NEWS_PAPERS WHERE name = ?", (name,))
    result = cursor.fetchone()
    
    db_connection.close()
    
    if result:
        return result[0]
    return None

def add_article(news_paper_id: int, title: str, content: str, publication_date: str) -> int:
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
