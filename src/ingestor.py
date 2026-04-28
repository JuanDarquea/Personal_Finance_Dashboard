import sys
from pathlib import Path

# Add parent directory to path so src modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
import pandas as pd
from src.categories import categorize
from src.db import insert_transactions


def ingest_csv(conn: sqlite3.Connection, csv_path: Path, source: str = "") -> int:
    """
    Parse a bank CSV, assign categories, and insert into the database.
    Expects columns: Date, Description, Amount.
    Returns the number of newly inserted rows.
    """
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # Normalize date to YYYY-MM-DD
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # Normalize amount to float
    df["amount"] = pd.to_numeric(
        df["amount"].astype(str).str.replace(",", ""), errors="coerce"
    )
    df = df.dropna(subset=["amount"])

    source_name = source or Path(csv_path).stem

    rows = [
        {
            "date": row["date"],
            "description": str(row["description"]).strip(),
            "amount": float(row["amount"]),
            "category": categorize(str(row["description"])),
            "source": source_name,
        }
        for _, row in df.iterrows()
    ]

    return insert_transactions(conn, rows)
