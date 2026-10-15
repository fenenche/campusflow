"""Tests for expanded report metrics and empty-data safety."""

import unittest
from campusflow.reports import generate_report


class ExtendedReportTests(unittest.TestCase):
    def test_category_counts_include_zero_categories(self):
        report = generate_report([
            {"status": "open", "priority": "high", "category": "Network"},
            {"status": "resolved", "priority": "low", "category": "Hardware"},
            {"status": "open", "priority": "medium", "category": "network"},
        ])
        self.assertEqual(report["by_category"], {"Network": 2, "Hardware": 1, "Software": 0, "Other": 0})

    def test_resolution_percentage_and_unresolved_breakdown(self):
        report = generate_report([
            {"status": "resolved", "priority": "high", "category": "Network"},
            {"status": "open", "priority": "low", "category": "Other"},
            {"status": "in_progress", "priority": "medium", "category": "Software"},
            {"status": "resolved", "priority": "critical", "category": "Hardware"},
        ])
        self.assertEqual(report["resolution_percentage"], 50.0)
        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["unresolved_by_status"], {"open": 1, "in_progress": 1})

    def test_empty_report_has_zero_metrics(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["unresolved_by_status"], {"open": 0, "in_progress": 0})
        self.assertTrue(all(value == 0 for value in report["by_category"].values()))

    def test_unknown_category_rejected(self):
        with self.assertRaises(ValueError):
            generate_report([{"status": "open", "priority": "low", "category": "Food"}])


if __name__ == "__main__":
    unittest.main()
