# seed_db.py
import sqlite3
from datetime import datetime

def seed_database(db_path="db.sqlite3"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert dummy sessions
    sessions = [
        ("2025-11-20", "10:00:00", "11:00:00", 5, 1),
        ("2025-11-21", "14:00:00", "15:00:00", 10, 1),
        ("2025-11-22", "09:00:00", "10:30:00", 8, 1),
    ]
    cursor.executemany(
        """
        INSERT INTO homepage_session (date, start_time, end_time, capacity, is_active)
        VALUES (?, ?, ?, ?, ?)
        """,
        sessions,
    )

    # Insert dummy signups
    signups = [
        ("Alice Johnson", "alice@example.com", 1, datetime.now().isoformat(), "active", "easy"),
        ("Bob Smith", "bob@example.com", 1, datetime.now().isoformat(), "active", "medium"),
        ("Charlie Brown", "charlie@example.com", 2, datetime.now().isoformat(), "active", "easy"),
        ("Dana White", "dana@example.com", 2, datetime.now().isoformat(), "canceled", "medium"),
        ("Eve Adams", "eve@example.com", 3, datetime.now().isoformat(), "active", "easy"),
    ]
    cursor.executemany(
        """
        INSERT INTO homepage_signup (name, email, session_id, created_at, status, lc_level)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        signups,
    )

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
