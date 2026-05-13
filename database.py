import sqlite3
import json

DB_NAME = "history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        job_description TEXT,
        results TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_history(job_title, job_description, results):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO history (job_title, job_description, results) VALUES (?, ?, ?)",
            (job_title, job_description, json.dumps(results))
        )

        conn.commit()
    except Exception as e:
        print("DB Error:", e)
    finally:
        conn.close()


def get_all_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        try:
            results = json.loads(row[3])
        except:
            results = []

        data.append({
            "id": row[0],
            "job_title": row[1],
            "job_description": row[2],
            "results": results
        })

    conn.close()
    return data


# MISSING — this function did not exist
def delete_history(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()