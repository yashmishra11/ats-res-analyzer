"""
Database Module
SQLite database for resume storage and system settings
"""

import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager


DB_FILE = "ats_analyzer.db"


@contextmanager
def get_db():
    """Context manager for database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                s3_url TEXT NOT NULL,
                file_size INTEGER,
                match_score REAL,
                expected_score REAL,
                user_email TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # System settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Initialize default settings
        cursor.execute("""
            INSERT OR IGNORE INTO system_settings (key, value)
            VALUES ('uploads_enabled', 'true')
        """)
        
        conn.commit()


def save_resume(filename, s3_url, match_score=None, expected_score=None, user_email=None):
    """Save resume metadata to database"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Try to get file size from S3 URL (estimate)
        file_size = 0  # Will be populated if needed
        
        cursor.execute("""
            INSERT INTO resumes (filename, s3_url, file_size, match_score, expected_score, user_email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, s3_url, file_size, match_score, expected_score, user_email))
        
        conn.commit()
        return cursor.lastrowid


def get_all_resumes():
    """Get all resumes from database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM resumes
            ORDER BY uploaded_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


def get_resumes_by_timeframe(start_time=None):
    """Get resumes within a specific timeframe"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        if start_time:
            cursor.execute("""
                SELECT * FROM resumes
                WHERE uploaded_at >= ?
                ORDER BY uploaded_at DESC
            """, (start_time,))
        else:
            cursor.execute("""
                SELECT * FROM resumes
                ORDER BY uploaded_at DESC
            """)
        
        return [dict(row) for row in cursor.fetchall()]


def get_upload_stats(start_time=None):
    """Get upload statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Total uploads
        if start_time:
            cursor.execute("""
                SELECT COUNT(*) as count FROM resumes
                WHERE uploaded_at >= ?
            """, (start_time,))
            recent_uploads = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM resumes")
            total_uploads = cursor.fetchone()['count']
        else:
            cursor.execute("SELECT COUNT(*) as count FROM resumes")
            total_uploads = cursor.fetchone()['count']
            recent_uploads = 0
        
        # Average score
        cursor.execute("""
            SELECT AVG(match_score) as avg_score
            FROM resumes
            WHERE match_score IS NOT NULL
        """)
        avg_score = cursor.fetchone()['avg_score']
        
        # Total storage (file sizes)
        cursor.execute("""
            SELECT SUM(file_size) as total_size
            FROM resumes
        """)
        total_size = cursor.fetchone()['total_size'] or 0
        total_size_mb = total_size / (1024 * 1024)
        
        # Unique users
        cursor.execute("""
            SELECT COUNT(DISTINCT user_email) as unique_users
            FROM resumes
            WHERE user_email IS NOT NULL
        """)
        unique_users = cursor.fetchone()['unique_users']
        
        return {
            'total_uploads': total_uploads,
            'recent_uploads': recent_uploads,
            'average_score': avg_score,
            'total_size_mb': total_size_mb,
            'unique_users': unique_users
        }


def get_system_settings():
    """Get all system settings as dictionary"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM system_settings")
        
        settings = {}
        for row in cursor.fetchall():
            key = row['key']
            value = row['value']
            
            # Parse boolean values
            if value.lower() in ('true', 'false'):
                settings[key] = value.lower() == 'true'
            else:
                settings[key] = value
        
        return settings


def update_system_settings(key, value):
    """Update a system setting"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Convert boolean to string
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        
        cursor.execute("""
            INSERT OR REPLACE INTO system_settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        
        conn.commit()


def is_uploads_enabled():
    """Check if uploads are currently enabled"""
    settings = get_system_settings()
    return settings.get('uploads_enabled', True)


def get_user_resumes(user_email, limit=10):
    """Get resumes for a specific user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM resumes
            WHERE user_email = ?
            ORDER BY uploaded_at DESC
            LIMIT ?
        """, (user_email, limit))
        
        return [dict(row) for row in cursor.fetchall()]