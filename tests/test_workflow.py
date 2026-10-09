import unittest
from campusflow.workflow import add_ticket, assign_ticket, update_ticket_status, priority_queue, next_ticket_id
from campusflow.reports import generate_report


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = {}
        self.low = add_ticket(self.tickets, "One", "Network", "low", 1)
        self.critical = add_ticket(self.tickets, "Two", "Software", "high", 12)
        self.high = add_ticket(self.tickets, "Three", "Hardware", "high", 2)

    def test_auto_ids_are_unique(self):
        self.assertEqual([self.low["id"], self.critical["id"], self.high["id"]], ["T001", "T002", "T003"])
        del self.tickets["T002"]
        self.assertEqual(next_ticket_id(self.tickets), "T004")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaisesRegex(ValueError, "Assign the ticket"):
            update_ticket_status(self.tickets, "T001", "in_progress")

    def test_assigned_ticket_can_progress_and_resolve(self):
        assign_ticket(self.tickets, "T001", "  Alex  ")
        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets["T001"]["assigned_to"], "Alex")
        self.assertEqual(self.tickets["T001"]["status"], "resolved")

    def test_blank_assignee_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "  ")

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Alex")

    def test_invalid_transition_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "resolved")

    def test_priority_queue_order(self):
        self.assertEqual([t["id"] for t in priority_queue(self.tickets)], ["T002", "T003", "T001"])

    def test_queue_ties_use_numeric_id(self):
        tickets = {}
        add_ticket(tickets, "first", "Other", "low", 1)
        add_ticket(tickets, "second", "Other", "low", 2)
        self.assertEqual([t["id"] for t in priority_queue(tickets)], ["T001", "T002"])

    def test_report_counts(self):
        report = generate_report(self.tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_status"]["open"], 3)

    def test_reopen_resolved_ticket(self):
        assign_ticket(self.tickets, "T001", "Alex")
        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")
        update_ticket_status(self.tickets, "T001", "open")
        self.assertEqual(self.tickets["T001"]["status"], "open")


if __name__ == "__main__":
    unittest.main()
