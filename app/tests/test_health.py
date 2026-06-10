from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase


class HealthViewTests(TestCase):
    def test_health_returns_ok_when_database_is_available(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "database": "available"},
        )

    @patch("app.views.connection.cursor")
    def test_health_returns_503_when_database_is_unavailable(self, mock_cursor):
        mock_cursor.side_effect = DatabaseError("database unavailable")

        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"status": "error", "database": "unavailable"},
        )
