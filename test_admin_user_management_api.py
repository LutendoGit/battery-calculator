#!/usr/bin/env python3
"""Automated tests for admin user-management API endpoints."""

from __future__ import annotations

import os
import tempfile
import unittest

from app import app
from modules import education_store


class AdminUserManagementApiTests(unittest.TestCase):
    """Covers auth + CRUD-style admin user-management endpoints."""

    def setUp(self) -> None:
        self.admin_token = "test-admin-token"
        os.environ["ADMIN_STREAM_TOKEN"] = self.admin_token

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

        # Seed three users for endpoint tests.
        self.user1 = education_store.create_user(
            "user_alpha", "password123", email="alpha@example.com"
        )
        self.user2 = education_store.create_user(
            "user_bravo", "password123", email="bravo@example.com"
        )
        self.user3 = education_store.create_user(
            "user_charlie", "password123", email="charlie@example.com"
        )

        # Seed activity for user1 so stats/history endpoints have meaningful data.
        self.login1 = education_store.track_login(
            self.user1.id, session_id="sess-alpha-1", ip_address="127.0.0.1"
        )
        education_store.track_login(
            self.user1.id, session_id="sess-alpha-2", ip_address="127.0.0.2"
        )
        education_store.mark_progress(self.user1.id, "lesson:fundamentals")
        education_store.record_quiz_attempt(self.user1.id, "capacity-dod", 8, 10)

    def tearDown(self) -> None:
        education_store.db_path = self._orig_db_path
        education_store._DB_READY = self._orig_db_ready
        self._tmpdir.cleanup()

    def _url(self, path: str, *, with_token: bool = True) -> str:
        if with_token:
            separator = "&" if "?" in path else "?"
            return f"{path}{separator}token={self.admin_token}"
        return path

    def test_requires_admin_token(self) -> None:
        response = self.client.get("/learn/admin/api/users/list")
        self.assertEqual(response.status_code, 403)

    def test_users_list_returns_seeded_users(self) -> None:
        response = self.client.get(self._url("/learn/admin/api/users/list"))
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertIn("users", payload)
        usernames = {u["username"] for u in payload["users"]}
        self.assertIn("user_alpha", usernames)
        self.assertIn("user_bravo", usernames)
        self.assertIn("user_charlie", usernames)

    def test_user_stats_endpoint(self) -> None:
        response = self.client.get(self._url(f"/learn/admin/api/users/{self.user1.id}/stats"))
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertEqual(payload["user_id"], self.user1.id)
        self.assertGreaterEqual(payload["logins"], 2)
        self.assertGreaterEqual(payload["progress_items"], 1)
        self.assertGreaterEqual(payload["quizzes_taken"], 1)
        self.assertGreaterEqual(payload["total_events"], 1)

    def test_user_login_history_endpoint_respects_limit(self) -> None:
        response = self.client.get(
            self._url(f"/learn/admin/api/users/{self.user1.id}/logins?limit=1")
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertIn("logins", payload)
        self.assertEqual(len(payload["logins"]), 1)

    def test_current_sessions_endpoint(self) -> None:
        # Only one session stays active after this logout.
        education_store.track_logout(self.login1)

        response = self.client.get(self._url("/learn/admin/api/sessions/current"))
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertIn("sessions", payload)
        self.assertEqual(len(payload["sessions"]), 1)
        self.assertEqual(payload["sessions"][0]["user_id"], self.user1.id)

    def test_logins_summary_endpoint(self) -> None:
        response = self.client.get(self._url("/learn/admin/api/logins/summary"))
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertEqual(payload["total_users"], 3)
        self.assertGreaterEqual(payload["active_sessions"], 1)
        self.assertIn("logins_today", payload)
        self.assertIn("avg_session_duration_minutes", payload)

    def test_reset_user_progress_endpoint(self) -> None:
        response = self.client.post(
            self._url(f"/learn/admin/api/users/{self.user1.id}/reset-progress")
        )
        self.assertEqual(response.status_code, 200)

        stats = education_store.get_user_stats(self.user1.id)
        self.assertEqual(stats["progress_items"], 0)
        self.assertEqual(stats["quizzes_taken"], 0)

    def test_delete_user_endpoint(self) -> None:
        response = self.client.delete(self._url(f"/learn/admin/api/users/{self.user2.id}"))
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertEqual(payload["status"], "deleted")
        self.assertIsNone(education_store.get_user(self.user2.id))

    def test_delete_user_not_found(self) -> None:
        response = self.client.delete(self._url("/learn/admin/api/users/99999"))
        self.assertEqual(response.status_code, 404)

    def test_bulk_delete_users_endpoint(self) -> None:
        response = self.client.post(
            self._url("/learn/admin/api/users/bulk-delete"),
            json={"user_ids": [self.user2.id, self.user3.id, 99999]},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()

        self.assertEqual(payload["total"], 3)
        self.assertEqual(payload["deleted"], 2)
        self.assertEqual(payload["failed"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
