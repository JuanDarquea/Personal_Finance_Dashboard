import sqlite3
import pandas as pd


def init_db(conn: sqlite3.Connection) -> None:
    """Create the transactions table if it doesn't exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT    NOT NULL,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            source      TEXT,
            UNIQUE(date, description, amount)
        )
    """)
    conn.commit()


def insert_transactions(conn: sqlite3.Connection, rows: list[dict]) -> int:
    """Insert rows, silently skip duplicates. Returns count of newly inserted rows."""
    cursor = conn.cursor()
    inserted = 0
    for row in rows:
        try:
            cursor.execute(
                "INSERT INTO transactions (date, description, amount, category, source) VALUES (?, ?, ?, ?, ?)",
                (row["date"], row["description"], row["amount"], row["category"], row.get("source", "")),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # duplicate — skip
    conn.commit()
    return inserted


def get_all_transactions(conn: sqlite3.Connection) -> pd.DataFrame:
    """Return all transactions as a DataFrame."""
    return pd.read_sql_query(
        "SELECT id, date, description, amount, category, source FROM transactions ORDER BY date DESC",
        conn,
    )


def get_monthly_summary(conn: sqlite3.Connection, month: str) -> dict[str, float]:
    """Return {category: total_amount} for a given month string (e.g. '2026-03')."""
    df = pd.read_sql_query(
        "SELECT category, SUM(amount) as total FROM transactions WHERE date LIKE ? GROUP BY category",
        conn,
        params=(f"{month}%",),
    )
    return dict(zip(df["category"], df["total"]))


def get_connection(db_path: str = "finance.db") -> sqlite3.Connection:
    """Open (or create) the SQLite database file and initialize schema."""
    conn = sqlite3.connect(db_path)
    init_db(conn)
    return conn
