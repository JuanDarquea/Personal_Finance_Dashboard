from src.db import insert_transactions, get_all_transactions, get_monthly_summary
import pandas as pd


SAMPLE_ROWS = [
    {"date": "2026-03-01", "description": "Whole Foods", "amount": -82.45, "category": "Groceries", "source": "bank_a"},
    {"date": "2026-03-04", "description": "Salary",      "amount": 2500.0, "category": "Income",    "source": "bank_a"},
    {"date": "2026-03-05", "description": "Netflix",     "amount": -15.99, "category": "Subscriptions", "source": "bank_a"},
]


def test_insert_and_retrieve(db_conn):
    insert_transactions(db_conn, SAMPLE_ROWS)
    df = get_all_transactions(db_conn)
    assert len(df) == 3
    assert list(df.columns) == ["id", "date", "description", "amount", "category", "source"]


def test_no_duplicate_insert(db_conn):
    insert_transactions(db_conn, SAMPLE_ROWS)
    insert_transactions(db_conn, SAMPLE_ROWS)  # insert same rows again
    df = get_all_transactions(db_conn)
    assert len(df) == 3  # still 3, not 6


def test_monthly_summary(db_conn):
    insert_transactions(db_conn, SAMPLE_ROWS)
    summary = get_monthly_summary(db_conn, "2026-03")
    assert summary["Groceries"] == -82.45
    assert summary["Income"] == 2500.0
