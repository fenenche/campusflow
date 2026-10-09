import unittest
from campusflow.tickets import calculate_priority, create_ticket, validate_ticket_data


class PriorityTests(unittest.TestCase):
    def test_high_and_twelve_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_and_two_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_and_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_and_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 0)

    def test_bool_is_not_an_integer_for_user_count(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", True)

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 2)

    def test_fields_are_normalized(self):
        ticket = validate_ticket_data("  Wi-Fi  ", "nEtWoRk", "HIGH", 2)
        self.assertEqual(ticket["title"], "Wi-Fi")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")

    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(" ", "Network", "low", 1, "T001")

    def test_ticket_defaults(self):
        ticket = create_ticket("Laptop issue", "Hardware", "medium", 1, "T001")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(ticket["id"], "T001")


if __name__ == "__main__":
    unittest.main()
