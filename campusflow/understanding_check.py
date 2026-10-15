"""Six-question interactive check of CampusFlow engineering contracts."""

from __future__ import annotations

from typing import Callable

QUESTIONS = (
    ("Why must a rejected operation leave the ticket collection unchanged?",
     ("Avoid printing an error", "Preserve data integrity and prevent partial state changes", "Reset ticket IDs to 1", "Make JSON files smaller"), "B"),
    ("What happens when adding a note to a resolved ticket?",
     ("Add the note and silently reopen it", "Delete existing notes", "Reject until explicitly reopened", "Change status to in_progress"), "C"),
    ("What does AND semantics mean for category and status filters?",
     ("Either filter may match", "Ignore category", "Both filters must match", "Return every ticket"), "C"),
    ("How does title-substring search behave?",
     ("Exact and case-sensitive only", "Substring match without regard to letter case", "Change stored title to lowercase", "Search ticket IDs only"), "B"),
    ("What should happen to a legacy ticket with no notes field?",
     ("Reject the whole file", "Delete the ticket", "Preserve compatibility and treat notes as absent/empty", "Overwrite data with an empty list"), "C"),
    ("Why run the full test suite after integration?",
     ("Prove the feature has the most lines", "Check integration and preserve existing behavior", "Avoid code review", "Replace regression tests"), "B"),
)

def result_band(score: int) -> str:
    """Map a score from 0 through 6 to the documented result band."""
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 6:
        raise ValueError("Score must be an integer from 0 to 6.")
    if score >= 5:
        return "Pass"
    if score >= 3:
        return "Review recommended"
    return "Revisit the design and implementation"


def run_understanding_check(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> dict[str, int | str]:
    """Ask six multiple-choice questions, retry invalid choices, and report score."""
    score = 0
    for index, (question, options, answer) in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {index}/6: {question}")
        for letter, option in zip("ABCD", options):
            output_fn(f"  {letter}. {option}")
        while True:
            selected = input_fn("Answer (A/B/C/D): ").strip().upper()
            if selected in {"A", "B", "C", "D"}:
                break
            output_fn("Invalid answer. Enter A, B, C, or D.")
        if selected == answer:
            score += 1
    band = result_band(score)
    output_fn(f"Result: {score}/6 — {band}")
    return {"score": score, "total": 6, "result": band}