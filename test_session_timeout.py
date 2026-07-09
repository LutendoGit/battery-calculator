#!/usr/bin/env python3
"""Automated tests for education session inactivity timeout behavior."""

from __future__ import annotations

import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

from app import app
from modules import education_store


class SessionTimeoutTests(unittest.TestCase):
    """Verifies auto-logout after 24 hours of inactivity."""

    def setUp(self) -> None:
        # Use a throwaway DB for tests so real app data is never modified.
        self._tmpdir = tempfile.TemporaryDirectory()
        self._test_db = os.path.join(self._tmpdir.name, "education_test.db")
        self._orig_db_path = education_store.db_path
        self._orig_db_ready = education_store._DB_READY
        education_store.db_path = lambda: self._test_db
        education_store._DB_READY = False
        education_store.ensure_db()

        app.config["TESTING"] = True
        self.client = app.test_client()

        self.user = education_store.create_user(
            "timeout_user", "password123", email="timeout@example.com"
        )

    def tearDown(self) -> None:
        education_store.db_path = self._orig_db_path
        education_store._DB_READY = self._orig_db_ready
        self._tmpdir.cleanup()

    def _set_logged_in_session(self, *, login_id: int, last_activity_iso: str) -> None:
        with self.client.session_transaction() as sess:
            sess["edu_user_id"] = self.user.id
            sess["edu_username"] = self.user.username
            sess["edu_avatar"] = self.user.avatar_filename
            sess["login_id"] = int(login_id)
            sess["edu_last_activity_at"] = last_activity_iso

    def _get_login_record(self, login_id: int) -> dict:
        rows = education_store.get_user_login_history(self.user.id, limit=20)
        for row in rows:
            if int(row.get("id") or 0) == int(login_id):
                return row
        return {}

    def test_page_request_auto_logs_out_after_24h_inactivity(self) -> None:
        login_id = education_store.track_login(self.user.id, session_id="timeout-page")
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=24, minutes=1)).isoformat()
        self._set_logged_in_session(login_id=login_id, last_activity_iso=old_ts)

        response = self.client.get("/learn/progress", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/learn/login", response.headers.get("Location", ""))

        with self.client.session_transaction() as sess:
            self.assertNotIn("edu_user_id", sess)
            self.assertNotIn("login_id", sess)
            self.assertNotIn("edu_last_activity_at", sess)

        login_row = self._get_login_record(login_id)
        self.assertTrue(login_row)
        self.assertIsNotNone(login_row.get("logout_at"))

    def test_api_request_returns_401_after_24h_inactivity(self) -> None:
        login_id = education_store.track_login(self.user.id, session_id="timeout-api")
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()
        self._set_logged_in_session(login_id=login_id, last_activity_iso=old_ts)

        response = self.client.get("/learn/api/quiz/unlock-state")

        self.assertEqual(response.status_code, 401)
        payload = response.get_json() or {}
        self.assertEqual(payload.get("error"), "session_expired_inactive")

        with self.client.session_transaction() as sess:
            self.assertNotIn("edu_user_id", sess)
            self.assertNotIn("login_id", sess)
            self.assertNotIn("edu_last_activity_at", sess)

        login_row = self._get_login_record(login_id)
        self.assertTrue(login_row)
        self.assertIsNotNone(login_row.get("logout_at"))

    def test_activity_within_timeout_keeps_session_and_refreshes_timestamp(self) -> None:
        login_id = education_store.track_login(self.user.id, session_id="timeout-keepalive")
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        self._set_logged_in_session(login_id=login_id, last_activity_iso=old_ts)

        response = self.client.get("/learn/api/quiz/unlock-state")

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            self.assertEqual(int(sess.get("edu_user_id")), int(self.user.id))
            refreshed = str(sess.get("edu_last_activity_at") or "")
            self.assertTrue(refreshed)
            refreshed_dt = datetime.fromisoformat(refreshed)
            if refreshed_dt.tzinfo is None:
                refreshed_dt = refreshed_dt.replace(tzinfo=timezone.utc)
            old_dt = datetime.fromisoformat(old_ts)
            self.assertGreater(refreshed_dt, old_dt)

        login_row = self._get_login_record(login_id)
        self.assertTrue(login_row)
        self.assertIsNone(login_row.get("logout_at"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
