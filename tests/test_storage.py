import json
import tempfile
import unittest
from pathlib import Path
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import add_ticket, next_ticket_id


class StorageTests(unittest.TestCase):
    def test_save_and_reload_preserves_tickets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nested" / "tickets.json"
            tickets = {}
            add_ticket(tickets, "Wi-Fi", "Network", "high", 12)
            save_tickets(tickets, path)
            self.assertEqual(load_tickets(path), tickets)

    def test_missing_file_returns_empty_dictionary(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(load_tickets(Path(folder) / "missing.json"), {})

    def test_corrupted_json_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_tickets(path)

    def test_non_object_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_create_after_reload_does_not_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = {}
            add_ticket(tickets, "First", "Other", "low", 1)
            save_tickets(tickets, path)
            restored = load_tickets(path)
            next_ticket = add_ticket(restored, "Second", "Other", "low", 1)
            self.assertEqual(next_ticket["id"], "T002")
            self.assertEqual(len(restored), 2)


if __name__ == "__main__":
    unittest.main()
