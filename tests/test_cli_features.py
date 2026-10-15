"""CLI tests for search/filter and structured ticket notes."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main as cli


class CliFeatureTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [{
            "id": 1, "title": "Campus WiFi", "category": "Network",
            "urgency": "high", "affected_users": 10, "priority": "critical",
            "status": "open", "assigned_to": None,
        }]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "tickets.json"

    def test_search_menu_displays_case_insensitive_match(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["WIFI", "", "", ""]), redirect_stdout(output):
            cli.search_tickets_menu(self.tickets)
        self.assertIn("Matching tickets: 1", output.getvalue())
        self.assertIn("Campus WiFi", output.getvalue())

    def test_search_menu_reports_invalid_filter(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["", "Food", "", ""]), redirect_stdout(output):
            cli.search_tickets_menu(self.tickets)
        self.assertIn("Error:", output.getvalue())

    def test_view_notes_handles_legacy_ticket_without_notes(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["1", "1"]), redirect_stdout(output):
            cli.manage_notes_menu(self.tickets, self.path)
        self.assertIn("No notes", output.getvalue())

    def test_add_notes_persists_structured_note(self):
        with patch("builtins.input", side_effect=["1", "2", " Bront ", " Checked the router "]):
            with redirect_stdout(io.StringIO()):
                cli.manage_notes_menu(self.tickets, self.path)
        self.assertEqual(self.tickets[0]["notes"], [{"author": "Bront", "message": "Checked the router"}])
        self.assertTrue(self.path.exists())

    def test_resolved_ticket_note_is_rejected_without_mutation(self):
        self.tickets[0]["status"] = "resolved"
        before = [dict(self.tickets[0])]
        with patch("builtins.input", side_effect=["1", "2", "Bront", "Not allowed"]), redirect_stdout(io.StringIO()):
            cli.manage_notes_menu(self.tickets, self.path)
        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()
