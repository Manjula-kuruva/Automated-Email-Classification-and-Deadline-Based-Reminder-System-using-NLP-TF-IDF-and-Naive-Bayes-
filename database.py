import sqlite3

DB_NAME = "events.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT,
            event_title TEXT,
            event_start TEXT,
            event_end TEXT,
            google_event_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_event(sender_email, event_title, start_time, end_time, google_event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (
            sender_email,
            event_title,
            event_start,
            event_end,
            google_event_id
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        sender_email,
        event_title,
        start_time.isoformat(),
        end_time.isoformat(),
        google_event_id
    ))

    conn.commit()
    conn.close()
def get_event_by_summary(summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, google_event_id
        FROM events
        WHERE email_text = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (f"%{summary}%",))

    row = cursor.fetchone()
    conn.close()
    return row

def delete_event_from_db(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def get_event_by_sender(sender_email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, google_event_id
        FROM events
        WHERE sender_email = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (sender_email,))

    row = cursor.fetchone()
    conn.close()
    return row
