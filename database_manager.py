import sqlite3
from typing import Optional

import article
from news_paper import NewsPaper
 
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
        FOREIGN KEY(news_paper_id) REFERENCES NEWS_PAPERS(id) ON DELETE CASCADE
    )""")

    cursor.execute("DROP TABLE IF EXISTS article_changes")
    cursor.execute("""
    CREATE TABLE article_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL,
        change TEXT NOT NULL,
        change_timestamp TEXT NOT NULL,
        FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
    )""")

    db_connection.commit()
    db_connection.close()
    
if __name__ == "__main__":
    confirmation = input("This will delete the existing database and create a new one. Enter Y to continue...")
    if confirmation.upper() == "Y":
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

def add_article(news_paper_id: int, title: str, content: str) -> int:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("""
    INSERT OR IGNORE INTO articles (news_paper_id, title, content)
    VALUES (?, ?, ?)
    """, (news_paper_id, title, content))

    article_id = cursor.lastrowid
    
    db_connection.commit()
    db_connection.close()
    
    return article_id

def add_article_change(article_id: int, change: str, change_timestamp: str) -> int:
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

def get_article_by_title(title: str) -> Optional[article.Article]:
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
        )
    return None

def get_article_by_id(article_id: int) -> Optional[article.Article]:
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
        )
    return None

def get_all_articles_of_news_paper(news_paper_id: int) -> list[article.Article]:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT * FROM articles WHERE news_paper_id = ?", (news_paper_id,))
    results = cursor.fetchall()
    
    db_connection.close()

    articles = []
    for row in results:
        articles.append(article.Article(
            id=row[0],
            title=row[2],
            content=row[3],
        ))
    return articles

def get_all_news_papers() -> list[NewsPaper]:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT name, id FROM NEWS_PAPERS")
    results = cursor.fetchall()
    
    db_connection.close()

    return [NewsPaper(title=row[0], id=row[1]) for row in results]

def get_article_changes(article_id: int) -> list[dict]:
    db_connection = sqlite3.connect("swiss_news_articles.db")
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT change, change_timestamp FROM article_changes WHERE article_id = ?", (article_id,))
    results = cursor.fetchall()
    
    db_connection.close()

    changes = []
    for row in results:
        changes.append({
            "change": row[0],
            "change_timestamp": row[1]
        })
    return changes