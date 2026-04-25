import pytest
import sqlite3
from src.db import init_db


@pytest.fixture
def db_conn():
    """Provide an in-memory SQLite connection with schema initialized."""
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()
