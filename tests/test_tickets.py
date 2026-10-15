import unittest

from campusflow.tickets import (
    add_note,
    calculate_priority,
    create_ticket,
    find_ticket,
    get_next_ticket_id,
)

class TicketTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_create_using_expected_defaults(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )

        self.assertEqual(ticket["id"], 1)
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(ticket["priority"], "high")

    def test_creation_normalizes_category_and_urgency(self):
        ticket = create_ticket(
            self.tickets, "  Broken laptop  ", " HARDWARE ", " LOW ", 1
        )

        self.assertEqual(ticket["title"], "Broken laptop")
        self.assertEqual(ticket["category"], "Hardware")
        self.assertEqual(ticket["urgency"], "low")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "  ", "Other", "low", 1)
        self.assertEqual(self.tickets, [])

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Issue", "Electricity", "low", 1)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Issue", "Other", "urgent", 1)

    def test_invalid_affected_users_are_rejected(self):
        for value in (0, -1, 2.5, "3", True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    create_ticket(
                        self.tickets, "Issue", "Other", "low", value
                    )
        self.assertEqual(self.tickets, [])

    def test_priority_boundaries(self):
        self.assertEqual(calculate_priority("low", 2), "low")
        self.assertEqual(calculate_priority("low", 3), "medium")
        self.assertEqual(calculate_priority("low", 9), "medium")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("medium", 10), "high")

    def test_ticket_ids_increase(self):
        create_ticket(self.tickets, "First", "Other", "low", 1)
        create_ticket(self.tickets, "Second", "Other", "low", 1)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets], [1, 2]
        )
        self.assertEqual(get_next_ticket_id(self.tickets), 3)

    def test_find_ticket_returns_matching_record(self):
        created = create_ticket(
            self.tickets, "Issue", "Software", "medium", 3
        )

        self.assertIs(find_ticket(self.tickets, 1), created)

    def test_find_unknown_ticket_raises_key_error(self):
        with self.assertRaises(KeyError):
            find_ticket(self.tickets, 99)

    def test_add_note_trim_author_and_message(self):
        ticket = create_ticket(
            self.tickets, "Wifi Outage,", "Network", "high", 2
        )

        result = add_note(
            self.tickets, ticket["id"], "  Bront888  ", "  Investigating  "
        )

        self.assertIs(result, ticket)
        self.assertEqual(
            ticket["notes"],
            [{"author": "Bront888", "message": "Investigating"}],
        )

    def test_add_multiple_notes_preserves_existing_notes(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )

        add_note(self.tickets, ticket["id"], "Alex", "First update")
        add_note(self.tickets, ticket["id"], "Sam", "Second update")

        self.assertEqual(
            ticket["notes"],
            [
                {"author": "Alex", "message": "First update"},
                {"author": "Sam", "message": "Second update"},
            ],
        )

    def test_blank_author_is_rejected_without_mutation(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )
        before = [dict(item) for item in self.tickets]

        with self.assertRaises(ValueError):
            add_note(self.tickets, ticket["id"], "   ", "Investigating")

        self.assertEqual(self.tickets, before)

    def test_blank_message_is_rejected_without_mutation(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )
        before = [dict(item) for item in self.tickets]

        with self.assertRaises(ValueError):
            add_note(self.tickets, ticket["id"], "Bront888", "   ")

        self.assertEqual(self.tickets, before)

    def test_unknown_ticket_rejected_without_mutation(self):
        create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )
        before = [dict(item) for item in self.tickets]

        with self.assertRaises(KeyError):
            add_note(self.tickets, 999, "Bront888", "Investigating")

    def test_resolved_ticket_rejects_note_without_mutation(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )
        ticket["status"] = "resolved"
        before = dict(ticket)

        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                ticket["id"],
                "Bront888",
                "Investigating",
            )

        self.assertEqual(ticket, before)

    def test_malformed_existing_notes_rejected_without_mutation(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi outage", "Network", "high", 2
        )
        ticket["notes"] = "not a list"
        before = dict(ticket)

        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                ticket["id"],
                "Bront888",
                "Investigating",
            )

        self.assertEqual(ticket, before)

if __name__ == "__main__":
    unittest.main()



