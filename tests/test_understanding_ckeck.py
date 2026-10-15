"""Tests for the six-question Engineering Understanding Check."""

import unittest
from campusflow.understanding_check import QUESTIONS, result_band, run_understanding_check


class UnderstandingCheckTests(unittest.TestCase):
    def test_result_band_boundaries(self):
        self.assertEqual(result_band(6), "Pass")
        self.assertEqual(result_band(5), "Pass")
        self.assertEqual(result_band(4), "Review recommended")
        self.assertEqual(result_band(3), "Review recommended")
        self.assertEqual(result_band(2), "Revisit the design and implementation")
        self.assertEqual(result_band(0), "Revisit the design and implementation")

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            result_band(7)

    def test_all_correct_answers_score_six(self):
        answers = iter([q[2] for q in QUESTIONS])
        output = []
        result = run_understanding_check(lambda _prompt: next(answers), output.append)
        self.assertEqual(result, {"score": 6, "total": 6, "result": "Pass"})
        self.assertTrue(any("6/6" in line for line in output))

    def test_all_wrong_answers_score_zero(self):
        answers = iter(["A" if q[2] != "A" else "B" for q in QUESTIONS])
        result = run_understanding_check(lambda _prompt: next(answers), lambda _line: None)
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["result"], "Revisit the design and implementation")

    def test_invalid_answer_reprompts_without_scoring(self):
        answers = iter(["X", "B", "C", "C", "B", "C", "B"])
        output = []
        result = run_understanding_check(lambda _prompt: next(answers), output.append)
        self.assertEqual(result["score"], 6)
        self.assertTrue(any("Invalid answer" in line for line in output))


if __name__ == "__main__":
    unittest.main()