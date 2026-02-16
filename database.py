import sqlite3

def init_db():
    conn = sqlite3.connect("dev.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_url TEXT,
            match_score REAL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_resume(file_name, file_url, score):
    conn = sqlite3.connect("dev.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumes (file_name, file_url, match_score)
        VALUES (?, ?, ?)
    """, (file_name, file_url, score))

    conn.commit()
    conn.close()
