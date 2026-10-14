# CampusFlow Baseline Check

## 1. Purpose

This document records the initial condition of CampusFlow before implementing the CampusFlow Next improvements.

## 2. Git Status

- Branch: main
- Working tree: Clean before documentation changes
- Local branch: Up to date with origin/main

## 3. Test Command

```bash
python3 -m unittest discover -s tests -v
```

## 4. Baseline Test Results

- Total tests: 25
- Passed: 25
- Failed: 0
- Errors: 0
- Result: OK

All 25 existing automated tests passed during the baseline check.

## 5. Existing Behaviour Verified

The existing tests cover:

1. Ticket creation and validation.
2. Priority calculation.
3. Rejection of blank ticket titles.
4. Prevention of starting work on unassigned tickets.
5. Ticket status transitions and reopening.
6. Priority queue ordering and numeric ID tie-breaking.
7. Saving and reloading tickets.
8. Rejection of corrupted JSON data.

## 6. Three Test Cases

| Test case | Expected behaviour |
|---|---|
| Create a ticket with a blank title | Reject the ticket |
| Move an unassigned ticket to in_progress | Reject the transition |
| Load corrupted JSON data | Raise a clear error |

These cases are covered by the existing automated tests.

## 7. Improvements to Investigate

CampusFlow Next requires investigation and verification of:

- Safe ticket assignment and status changes.
- Structured ticket notes.
- Ticket search and combined filters.
- Accurate reports and analytics.
- Safe JSON loading and ticket ID continuity.
- Additional automated tests and peer review.

These are areas to verify against the assignment requirements, not claims that every feature is currently broken.

## 8. Conclusion

The baseline test suite passed all 25 existing tests. Further testing is required to verify that the completed system meets all CampusFlow Next acceptance criteria.
