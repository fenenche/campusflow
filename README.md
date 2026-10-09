# CampusFlow — CLI Helpdesk Ticket Manager

CampusFlow is a small Python command-line app for recording campus IT support tickets, assigning staff, tracking status, ordering work by priority, producing summary reports, and preserving tickets in JSON.

## Requirements
- Python 3.10 or newer
- No third-party packages

## Run the app
From the repository root:

```bash
python main.py
```

Tickets are saved to `data/tickets.json` when changes are made and when you exit. The `data/` directory is created automatically.

## Run automated tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers priority rules, invalid inputs, ticket creation, assignment, status transitions, queue ordering, reports, and JSON persistence.

## Ticket rules
- Categories: Network, Hardware, Software, Other (case-insensitive input; normalized for storage).
- Urgency: low, medium, high (case-insensitive input; normalized for storage).
- Affected-user count must be a positive integer; booleans are rejected by the Python API.
- Priority rules are applied in order: high + 10 or more users → critical; high OR 10+ users → high; medium OR 3+ users → medium; otherwise low.
- A ticket must be assigned before it can move from `open` to `in_progress`; it can then move to `resolved`. Resolved tickets can be reopened.

## Project layout

```text
campusflow/
  __init__.py
  tickets.py       # validation and priority calculation
  workflow.py      # ID generation, assignment, lifecycle, queue
  storage.py       # JSON persistence
  reports.py       # summary reports
tests/
  test_tickets.py
  test_workflow.py
  test_storage.py
main.py             # CLI
 docs/
  design-decisions.md
  ai-learning-log.md
```

## Git workflow and evidence
Use descriptive feature branches and pull requests; do not work directly on `main`. A teammate must inspect the code, leave substantive review feedback, and approve before a PR is merged. Record actual test output and genuine AI-learning experiences; do not claim a review, test run, or learning interaction that did not happen.
