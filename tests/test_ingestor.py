import sqlite3
import pytest
from pathlib import Path
from src.db import init_db, get_all_transactions
from src.ingestor import ingest_csv


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()


SAMPLE_CSV = Path("sample_data/sample_transactions.csv")


def test_ingest_csv_loads_rows(db_conn):
    count = ingest_csv(db_conn, SAMPLE_CSV)
    assert count == 20


def test_ingest_csv_assigns_categories(db_conn):
    ingest_csv(db_conn, SAMPLE_CSV)
    df = get_all_transactions(db_conn)
    assert "Groceries" in df["category"].values
    assert "Transport" in df["category"].values
    assert "Income" in df["category"].values


def test_ingest_csv_skips_duplicates(db_conn):
    ingest_csv(db_conn, SAMPLE_CSV)
    second_run = ingest_csv(db_conn, SAMPLE_CSV)
    assert second_run == 0


def test_ingest_csv_normalizes_date(db_conn):
    ingest_csv(db_conn, SAMPLE_CSV)
    df = get_all_transactions(db_conn)
    assert df["date"].str.match(r"\d{4}-\d{2}-\d{2}").all()
