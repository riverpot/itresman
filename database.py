import sqlite3
import contextlib
import os


def _db_path() -> str:
    return os.environ.get("DB_PATH", "itresman.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextlib.contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id           TEXT PRIMARY KEY,
                username     TEXT NOT NULL UNIQUE,
                email        TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                is_active    INTEGER NOT NULL DEFAULT 1,
                created_at   TEXT NOT NULL
            )
        """)
