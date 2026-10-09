import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import save_tickets, load_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        # Create a temporary folder for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "tickets.json"

        self.tickets = [
            {
                "id": "T001",
                "title": "Internet is not working",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

    def tearDown(self):
        # Remove the temporary folder after each test
        self.temp_dir.cleanup()

    def test_save_and_load_tickets(self):
        # Save tickets and load them back
        save_tickets(self.tickets, self.file_path)
        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, self.tickets)

    def test_load_missing_file_returns_empty_list(self):
        # A missing file should start with no tickets
        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, [])

    def test_invalid_json_raises_error(self):
        # Invalid JSON should raise a clear error
        self.file_path.write_text("{invalid json")

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_saved_file_contains_valid_json(self):
        # Confirm that saved data is valid JSON
        save_tickets(self.tickets, self.file_path)

        with self.file_path.open("r", encoding="utf-8") as file:
            loaded_data = json.load(file)

        self.assertEqual(loaded_data, self.tickets)


if __name__ == "__main__":
    unittest.main()