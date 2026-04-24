import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('symmetry_history.db')
    c = conn.cursor()
    # තීරණ ගබඩා කරන ටේබල් එක
    c.execute('''CREATE TABLE IF NOT EXISTS decisions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  entity TEXT,
                  market_price REAL,
                  vibe_score INTEGER,
                  status TEXT)''')
    conn.commit()
    conn.close()

def save_decision(entity, price, vibe, status):
    conn = sqlite3.connect('symmetry_history.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO decisions (timestamp, entity, market_price, vibe_score, status) VALUES (?, ?, ?, ?, ?)",
              (now, entity, price, vibe, status))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('symmetry_history.db')
    # මෙන්න මෙතනටයි Pandas ඕනේ කරන්නේ
    df = pd.read_sql_query("SELECT * FROM decisions ORDER BY id DESC LIMIT 5", conn)
    conn.close()
    return df