"""Simple SQLite-backed user accounts + progress tracking for the education module.

No external dependencies beyond Flask/Werkzeug.
"""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

from werkzeug.security import check_password_hash, generate_password_hash


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def db_path() -> str:
    return os.path.join(_project_root(), "data", "education.db")


_DB_READY = False


def ensure_db() -> None:
    global _DB_READY
    if _DB_READY:
        return

    path = db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    conn = sqlite3.connect(path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                user_id INTEGER NOT NULL,
                item_key TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                PRIMARY KEY (user_id, item_key),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                user_id INTEGER NOT NULL,
                quiz_id TEXT NOT NULL,
                best_score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                PRIMARY KEY (user_id, quiz_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()
        _DB_READY = True
    finally:
        conn.close()


def _connect() -> sqlite3.Connection:
    ensure_db()
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


@dataclass(frozen=True)
class User:
    id: int
    username: str


def create_user(username: str, password: str) -> User:
    username = (username or "").strip()
    if not username:
        raise ValueError("Username is required")
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")

    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters")

    password_hash = generate_password_hash(password)

    with _connect() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, _utc_now_iso()),
            )
        except sqlite3.IntegrityError as e:
            raise ValueError("Username already exists") from e
        user_id = int(cur.lastrowid)
        conn.commit()

    return User(id=user_id, username=username)


def authenticate_user(username: str, password: str) -> Optional[User]:
    username = (username or "").strip()
    if not username or not password:
        return None

    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row:
        return None

    if not check_password_hash(row["password_hash"], password):
        return None

    return User(id=int(row["id"]), username=str(row["username"]))


def get_user(user_id: int) -> Optional[User]:
    with _connect() as conn:
        row = conn.execute("SELECT id, username FROM users WHERE id = ?", (int(user_id),)).fetchone()
    if not row:
        return None
    return User(id=int(row["id"]), username=str(row["username"]))


def mark_progress(user_id: int, item_key: str) -> None:
    if not item_key:
        return
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO progress (user_id, item_key, completed_at) VALUES (?, ?, ?)",
            (int(user_id), str(item_key), _utc_now_iso()),
        )
        conn.commit()


def get_completed_items(user_id: int) -> set[str]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT item_key FROM progress WHERE user_id = ?",
            (int(user_id),),
        ).fetchall()
    return {str(r["item_key"]) for r in rows}


def record_quiz_attempt(user_id: int, quiz_id: str, score: int, total: int) -> None:
    quiz_id = (quiz_id or "").strip()
    if not quiz_id:
        return

    score = int(score)
    total = int(total)
    if total <= 0:
        return
    if score < 0:
        score = 0
    if score > total:
        score = total

    with _connect() as conn:
        existing = conn.execute(
            "SELECT best_score, total FROM quiz_attempts WHERE user_id = ? AND quiz_id = ?",
            (int(user_id), quiz_id),
        ).fetchone()

        best_score = score
        best_total = total
        if existing:
            prev_best = int(existing["best_score"])
            prev_total = int(existing["total"])
            prev_pct = (prev_best / prev_total) if prev_total else 0
            new_pct = (score / total) if total else 0
            if new_pct < prev_pct:
                best_score = prev_best
                best_total = prev_total

        conn.execute(
            "INSERT OR REPLACE INTO quiz_attempts (user_id, quiz_id, best_score, total, completed_at) VALUES (?, ?, ?, ?, ?)",
            (int(user_id), quiz_id, int(best_score), int(best_total), _utc_now_iso()),
        )
        conn.commit()


def get_quiz_best(user_id: int) -> dict[str, dict[str, int]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT quiz_id, best_score, total FROM quiz_attempts WHERE user_id = ?",
            (int(user_id),),
        ).fetchall()

    out: dict[str, dict[str, int]] = {}
    for r in rows:
        out[str(r["quiz_id"])] = {"best_score": int(r["best_score"]), "total": int(r["total"])}
    return out
