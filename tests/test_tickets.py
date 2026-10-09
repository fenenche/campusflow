"""Test for ticket creation and priority calculation."""

import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestCalculatePriority(unittest.TestCase):
    
    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 2),"high")

    def test_many_users_with_low_urgency_is_high(self):
        self.assertEqual(calculate_priority("low", 10),"high")
    
    def test_medium_urgency_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1),"medium")

    def test_three_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 3),"medium")

    def test_low_urgency_and_one_user_is_low(self):
        self.assertEqual(calculate_priority("low",1),"low")

    def test_zero_users_is_rejected(self):
       with self.assertRaises(ValueError):
         calculate_priority("low",0)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent",5)
    
class TestCreateTicket(unittest.TestCase):
    def test_ticket_has_all_required_fields(self):
        ticket = create_ticket(
            title="Cannot connect to Wi-Fi",
            category="Network",
            urgency="high",
            affected_users=12,
            ticket_id="T001",
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"],"critical")
        self.assertEqual(ticket["status"],"open")
        self.assertIsNone(ticket["assigned_to"])
    
    def test_blank_tittle_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                title=" ",
                category="Network",
                urgency="low",
                affected_users=1,
                ticket_id="T001",
            )

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                title="Printer problem",
                category="Invalid",
                urgency="low",
                affected_users=1,
                ticket_id="T001",
            )

if __name__ =="__main__":
    unitest.main()


    
    

    