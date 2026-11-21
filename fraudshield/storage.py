import sqlite3
import json
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "fraudshield.db"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            amount REAL,
            risk_score INTEGER,
            risk_level TEXT,
            decision TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            raw_json TEXT
        )
        """)

def save_transactions(frame):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        for record in frame.to_dict("records"):
            con.execute("""
            INSERT INTO transactions
            (transaction_id, amount, risk_score, risk_level, decision, raw_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(record.get("transaction_id", "N/A")),
                float(record.get("amount", 0)),
                int(record.get("risk_score", 0)),
                str(record.get("risk_level", "LOW")),
                str(record.get("decision", "NO ALERT")),
                json.dumps(record, default=str)
            ))

def load_transactions():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql_query("""
        SELECT transaction_id, amount, risk_score, risk_level, decision, created_at
        FROM transactions ORDER BY id DESC
        """, con)

def clear_history():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DELETE FROM transactions")
