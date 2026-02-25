"""SQLite-backed user accounts + progress tracking for the education module.

This module is intentionally small and dependency-light:
- Uses stdlib `sqlite3` for persistence.
- Uses `werkzeug.security` for password hashing and verification.

High-level responsibilities
--------------------------
- Create/authenticate users.
- Store progress/completion markers for learning items.
- Store best quiz attempts.
- Issue and consume one-time password reset tokens.

Notes
-----
- Timestamps are stored as ISO-8601 strings in UTC.
- A simple module-level flag avoids re-creating tables on every call.
"""

from __future__ import annotations

import os
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone 
from typing import Any, Iterable, Optional
import json
from werkzeug.security import check_password_hash, generate_password_hash


# Bump this when you ship changes to learning content/structure and want all
# existing users to restart learning progress from scratch.
_EDUCATION_CONTENT_VERSION = "2026-02-20_module1_fundamentals_v3_quiz_update"


def _ensure_content_version(conn: sqlite3.Connection) -> None:
    """Ensure the DB's education content version matches the running app.

    If the version differs, wipe progress + quiz attempts so all users start
    afresh with the new content.
    """

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    row = conn.execute("SELECT value FROM meta WHERE key = ?", ("education_content_version",)).fetchone()
    existing = str(row[0]) if row and row[0] is not None else ""

    if existing == _EDUCATION_CONTENT_VERSION:
        return

    # Reset learning progress for all users.
    conn.execute("DELETE FROM progress")
    conn.execute("DELETE FROM quiz_attempts")
    conn.execute(
        "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
        ("education_content_version", _EDUCATION_CONTENT_VERSION),
    )
    conn.commit()


def _utc_now_iso() -> str:
    """Return current time as an ISO-8601 UTC string (no microseconds).

    I store timestamps as strings in SQLite to keep the schema simple and
    portable across environments.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _project_root() -> str:
    """Return absolute path to the project root.

    This module lives in `modules/`, so project root is one level up.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def db_path() -> str:
    """Return the absolute path to the SQLite database file."""
    return os.path.join(_project_root(), "data", "education.db")


# Module-level cache so I only run CREATE TABLE statements once per process.
_DB_READY = False


def ensure_db() -> None:
    """Ensure required tables exist.

    This is safe to call many times; after the first successful run it becomes
    a fast no-op due to `_DB_READY`.
    """
    global _DB_READY
    if _DB_READY:
        return

    path = db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create the DB file (and parent folder) if missing.
    conn = sqlite3.connect(path)
    try:
         # Better concurrent read/write behavior for monitoring.
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA busy_timeout=5000;")



        # `users`: authentication data (passwords stored as hashes).
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                avatar_filename TEXT
            )
            """
        )

         conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                avatar_filename TEXT,
                email TEXT
            )
            """
        )

        # Migration for older DBs:
        try:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
            if "avatar_filename" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN avatar_filename TEXT")
            if "email" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
        except Exception:
            pass

        # Enforce email uniqueness (case-insensitive), but allow NULLs.
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_unique
            ON users(lower(email))
            WHERE email IS NOT NULL
            """
        )

        # Migration: older DBs won't have avatar_filename.
        try:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
            if "avatar_filename" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN avatar_filename TEXT")
        except Exception:
            # Best-effort migration; schema issues should not crash app startup.
            pass

        # `password_resets`: one-time reset tokens (stored as hashes).
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                secret_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                used_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

        # `progress`: completed learning items keyed by an item identifier.
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

        # `quiz_attempts`: best score recorded per quiz.
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

        
        # `user_events`: append-only stream for live monitoring + audit trail.
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_events_id ON user_events(id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_events_user ON user_events(user_id)")

        # Content versioning (wipes progress when content changes).
        _ensure_content_version(conn)


        # Persist DDL changes.
        conn.commit()
        _DB_READY = True
    finally:
        conn.close()


def _connect() -> sqlite3.Connection:
    """Open a SQLite connection with Row objects for dict-like access."""
    ensure_db()
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn
    
def record_event(event_type: str, *, user_id: Optional[int] = None, payload: Optional[dict[str, Any]] = None) -> None:
    event_type = (event_type or "").strip()
    if not event_type:
        return

    safe_payload = payload or {}

    try:
        normalized_user_id = int(user_id) if user_id is not None else None
    except Exception:
        normalized_user_id = None

    with _connect() as conn:
        try:
            conn.execute(
                "INSERT INTO user_events (user_id, type, payload, created_at) VALUES (?, ?, ?, ?)",
                (
                    normalized_user_id,
                    event_type,
                    json.dumps(safe_payload, separators=(",", ":"), ensure_ascii=False),
                    _utc_now_iso(),
                ),
            )
        except sqlite3.IntegrityError:
            conn.execute(
                "INSERT INTO user_events (user_id, type, payload, created_at) VALUES (?, ?, ?, ?)",
                (
                    None,
                    event_type,
                    json.dumps(safe_payload, separators=(",", ":"), ensure_ascii=False),
                    _utc_now_iso(),
                ),
            )
        conn.commit()

def get_events_since(after_id: int, *, limit: int = 200) -> list[dict[str, Any]]:
    """Fetch events with id > after_id."""
    after_id = int(after_id or 0)
    limit = max(1, min(int(limit or 200), 1000))

    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, user_id, type, payload, created_at "
            "FROM user_events WHERE id > ? ORDER BY id ASC LIMIT ?",
            (after_id, limit),
        ).fetchall()

    out: list[dict[str, Any]] = []
    for r in rows:
        payload_text = str(r["payload"] or "{}")
        try:
            payload_obj = json.loads(payload_text)
        except Exception:
            payload_obj = {"_raw": payload_text}

        out.append(
            {
                "id": int(r["id"]),
                "user_id": (int(r["user_id"]) if r["user_id"] is not None else None),
                "type": str(r["type"]),
                "payload": payload_obj,
                "created_at": str(r["created_at"]),
            }
        )
    return out

@dataclass(frozen=True)
class User:
    """Public user shape used by routes/UI.

    Intentionally does not expose password hashes or other sensitive fields.
    """
    id: int
    username: str
    avatar_filename: Optional[str] = None


def get_user_by_username(username: str) -> Optional[User]:
    """Look up a user by username.

    Returns None if `username` is empty/whitespace or not found.
    """
    username = (username or "").strip()
    if not username:
        return None
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, avatar_filename FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if not row:
        return None
    return User(
        id=int(row["id"]),
        username=str(row["username"]),
        avatar_filename=(str(row["avatar_filename"]) if row["avatar_filename"] else None),
    )


def create_user(username: str, password: str, *, avatar_filename: Optional[str] = None) -> User:
    """Create a new user account.

    Validation rules are kept simple to match the educational use case.
    Raises ValueError for user-facing validation errors.
    """
    username = (username or "").strip()
    if not username:
        raise ValueError("Username is required")
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")

    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters")

    # Store a salted hash (never the raw password).
    password_hash = generate_password_hash(password)

    with _connect() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO users (username, password_hash, created_at, avatar_filename) VALUES (?, ?, ?, ?)",
                (username, password_hash, _utc_now_iso(), (str(avatar_filename) if avatar_filename else None)),
            )
        except sqlite3.IntegrityError as e:
            # The UNIQUE constraint on username triggers this.
            raise ValueError("Username already exists") from e
        user_id = int(cur.lastrowid)
        conn.commit()

    return User(id=user_id, username=username, avatar_filename=(str(avatar_filename) if avatar_filename else None))


def authenticate_user(username: str, password: str) -> Optional[User]:
    """Validate credentials and return the matching user, else None."""
    username = (username or "").strip()
    if not username or not password:
        return None

    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, avatar_filename FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row:
        return None

    # Compare against the stored password hash.
    if not check_password_hash(row["password_hash"], password):
        return None

    user = User(
        id=int(row["id"]),
        username=str(row["username"]),
        avatar_filename=(str(row["avatar_filename"]) if row["avatar_filename"] else None),
    )
    # Log successful auth for live monitoring.
    record_event("login", user_id=user.id, payload={"username": user.username})
    return user


def update_user_password(user_id: int, new_password: str) -> None:
    """Set a user's password to `new_password` (stored as a hash)."""
    if not new_password or len(new_password) < 6:
        raise ValueError("Password must be at least 6 characters")
    password_hash = generate_password_hash(new_password)
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, int(user_id)),
        )
        conn.commit()


def set_user_avatar(user_id: int, avatar_filename: Optional[str]) -> User:
    """Set (or clear) a user's avatar filename.

    `avatar_filename` should be a filename under `static/avatars/` (not a path).
    """
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET avatar_filename = ? WHERE id = ?",
            ((str(avatar_filename) if avatar_filename else None), int(user_id)),
        )
        conn.commit()

    user = get_user(int(user_id))
    if not user:
        raise ValueError("User not found")
    return user


def create_password_reset(username: str, *, expires_in_seconds: int = 3600) -> Optional[str]:
    """Create a single-use password reset token for a username.

    Returns a token string if the user exists, otherwise returns None.

    Token format is: "<reset_id>.<secret>" where secret is random.
    """
    user = get_user_by_username(username)
    if not user:
        return None

    # Secret is what the user will present later; only its hash is stored.
    secret = secrets.token_urlsafe(32)
    secret_hash = generate_password_hash(secret)
    created_at = _utc_now_iso()
    expires_at = (
        datetime.now(timezone.utc).replace(microsecond=0)
        + timedelta(seconds=int(expires_in_seconds))
    ).isoformat()

    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO password_resets (user_id, secret_hash, created_at, expires_at, used_at) VALUES (?, ?, ?, ?, NULL)",
            (int(user.id), secret_hash, created_at, expires_at),
        )
        reset_id = int(cur.lastrowid)
        conn.commit()

    # Token is split into an ID and secret, so we can look up the row quickly.
    return f"{reset_id}.{secret}"


def consume_password_reset(token: str, new_password: str) -> Optional[User]:
    """Validate a reset token, set new password, and mark token used.

    Returns the user on success, otherwise None.
    """
    if not token or "." not in token:
        return None

    # Token format: "<reset_id>.<secret>".
    reset_id_str, secret = token.split(".", 1)
    if not reset_id_str.isdigit() or not secret:
        return None
    reset_id = int(reset_id_str)

    if not new_password or len(new_password) < 6:
        return None

    with _connect() as conn:
        # Load the reset row; if anything looks wrong we fail closed (return None).
        row = conn.execute(
            "SELECT id, user_id, secret_hash, expires_at, used_at FROM password_resets WHERE id = ?",
            (reset_id,),
        ).fetchone()

        if not row:
            return None

        if row["used_at"]:
            return None

        try:
            expires_at = datetime.fromisoformat(str(row["expires_at"]))
        except Exception:
            return None

        now = datetime.now(timezone.utc)
        # fromisoformat preserves timezone if present; ensure aware comparisons.
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= now:
            return None

        # Verify the presented secret against the stored hash.
        if not check_password_hash(str(row["secret_hash"]), secret):
            return None

        # Update password + consume token in the same transaction.
        new_password_hash = generate_password_hash(new_password)
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, int(row["user_id"])),
        )
        conn.execute(
            "UPDATE password_resets SET used_at = ? WHERE id = ?",
            (_utc_now_iso(), reset_id),
        )
        conn.commit()

    return get_user(int(row["user_id"]))


def get_user(user_id: int) -> Optional[User]:
    """Look up a user by numeric id."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, avatar_filename FROM users WHERE id = ?",
            (int(user_id),),
        ).fetchone()
    if not row:
        return None
    return User(
        id=int(row["id"]),
        username=str(row["username"]),
        avatar_filename=(str(row["avatar_filename"]) if row["avatar_filename"] else None),
    )


def mark_progress(user_id: int, item_key: str) -> None:
    """Mark a learning item as completed for the given user."""
    if not item_key:
        return
    
    item_key = str(item_key)
    completed_at = _utc_now_iso()

    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO progress (user_id, item_key, completed_at) VALUES (?, ?, ?)",
            (int(user_id), str(item_key),completed_at),
        )
        conn.commit()
    record_event("progress_marked", user_id=int(user_id), payload={"item_key": item_key, "completed_at": completed_at})
    


def get_completed_items(user_id: int) -> set[str]:
    """Return the set of completed item keys for a user."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT item_key FROM progress WHERE user_id = ?",
            (int(user_id),),
        ).fetchall()
    return {str(r["item_key"]) for r in rows}


def record_quiz_attempt(user_id: int, quiz_id: str, score: int, total: int) -> None:
    """Record a quiz attempt, keeping the best *percentage* score.

    If a user re-takes a quiz and gets a lower percentage, their prior best is
    kept.
    """
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
    
    completed_at = _utc_now_iso()
    improved = False

    with _connect() as conn:
        # i store per-user per-quiz best. Compare using percentage to handle
        # quizzes with differing totals over time.
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
            improved = new_pct > prev_pct
            if new_pct < prev_pct:
                best_score = prev_best
                best_total = prev_total
        else:
            improved = True

        conn.execute(
            "INSERT OR REPLACE INTO quiz_attempts (user_id, quiz_id, best_score, total, completed_at) VALUES (?, ?, ?, ?, ?)",
            (int(user_id), quiz_id, int(best_score), int(best_total), completed_at),
        )
        conn.commit()

    # Best-effort event recording; should never break quiz completion.
    try:
        record_event(
            "quiz_attempt",
            user_id=int(user_id),
            payload={
                "quiz_id": quiz_id,
                "score": int(score),
                "total": int(total),
                "best_score": int(best_score),
                "best_total": int(best_total),
                "improved": bool(improved),
                "completed_at": completed_at,
            },
        )
    except Exception:
        pass


def get_quiz_best(user_id: int) -> dict[str, dict[str, int]]:
    """Return best quiz results keyed by quiz_id."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT quiz_id, best_score, total FROM quiz_attempts WHERE user_id = ?",
            (int(user_id),),
        ).fetchall()

    out: dict[str, dict[str, int]] = {}
    for r in rows:
        out[str(r["quiz_id"])] = {"best_score": int(r["best_score"]), "total": int(r["total"])}
    return out
