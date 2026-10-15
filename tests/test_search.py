"""Regression tests for ticket search and AND-combined filters."""

import unittest
from campusflow.search import search_tickets


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": 1, "title": "Campus WiFi Problem", "category": "Network", "status": "open", "priority": "critical"},
            {"id": 2, "title": "Broken Laptop", "category": "Hardware", "status": "in_progress", "priority": "high"},
            {"id": 3, "title": "WiFi Password Help", "category": "Network", "status": "resolved", "priority": "low"},
        ]

    def test_empty_query_returns_all(self):
        self.assertEqual(search_tickets(self.tickets), self.tickets)

    def test_title_substring_is_case_insensitive(self):
        self.assertEqual([t["id"] for t in search_tickets(self.tickets, "WIFI")], [1, 3])

    def test_query_is_substring_not_exact_match(self):
        self.assertEqual([t["id"] for t in search_tickets(self.tickets, "Laptop")], [2])

    def test_no_match_returns_empty_list(self):
        self.assertEqual(search_tickets(self.tickets, "printer"), [])

    def test_category_filter_is_case_insensitive(self):
        self.assertEqual([t["id"] for t in search_tickets(self.tickets, category="network")], [1, 3])

    def test_status_filter(self):
        self.assertEqual([t["id"] for t in search_tickets(self.tickets, status="in_progress")], [2])

    def test_priority_filter(self):
        self.assertEqual([t["id"] for t in search_tickets(self.tickets, priority="high")], [2])

    def test_all_filters_use_and_semantics(self):
        result = search_tickets(self.tickets, "wifi", "Network", "open", "critical")
        self.assertEqual([t["id"] for t in result], [1])
        self.assertEqual(search_tickets(self.tickets, "wifi", "Network", "open", "low"), [])

    def test_invalid_filter_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="Food")

    def test_non_text_query_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, title_query=None)

    def test_search_does_not_mutate_collection(self):
        before = [dict(ticket) for ticket in self.tickets]
        search_tickets(self.tickets, "wifi", category="Network")
        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()
