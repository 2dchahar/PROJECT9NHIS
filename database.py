import sqlite3

conn = sqlite3.connect("data/queries.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    query TEXT,
    summary TEXT
)
""")

def save_query(query, summary):
    cursor.execute("INSERT INTO history VALUES (?, ?)", (query, summary))
    conn.commit()

def load_history():
    return cursor.execute("SELECT * FROM history").fetchall()
