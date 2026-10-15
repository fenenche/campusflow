# CampusFlow

CampusFlow is a standard-library Python command-line ticket tracker developed for the **CampusFlow Next — Guided Reliability, Search & Engineering Quality Sprint**.

## Current capabilities

- Create, view, validate, and prioritize support tickets.
- Assign tickets and enforce the ticket lifecycle: `open -> in_progress -> resolved`, with explicit reopening.
- Display an open-only queue sorted by priority and numeric ticket ID.
- Generate reports with status, priority, and category counts, resolution percentage, and unresolved-ticket counts.
- Add structured ticket notes and validate note data during JSON persistence.
- Search ticket titles case-insensitively and combine category, status, and priority filters using AND semantics.
- Provide a six-question Engineering Understanding Check.
- Persist ticket data to JSON with validation and clear storage errors.

## Constraints

- Python standard library only for the application and tests.
- `unittest` for automated tests and `json` for persistence.
- No database, web API, or third-party application framework.
- Business logic must be testable without interactive CLI prompts.

## Team and ownership

- **Engineer A — Bront888:** ticket validation/invariants, safe assignment and status mutation checks, structured notes, JSON validation, persistence/reload safety, and related regression tests.
- **Engineer B — Dorcas (`dinalegwu`):** title search, combined filters, expanded reports, notes CLI interaction, the six-question Engineering Understanding Check, and related tests.
- Both engineers contribute meaningful tests, record genuine AI-assisted learning with independent verification, review each other's pull requests, and verify the integrated application.

## Locked design decisions

- Queue policy: `open-only`.
- Resolved-ticket policy: mutations are blocked until an explicit reopen.
- Storage format: JSON, using the Python standard library.
- Invalid operations must not leave the ticket collection partially mutated.
- A ticket's structured `notes` field is a list of objects containing trimmed, nonblank `author` and `message` strings. Legacy tickets without `notes` remain valid.

See [docs/design-decisions.md](docs/design-decisions.md) for data contracts and acceptance rules, [docs/baseline-check.md](docs/baseline-check.md) for the recorded baseline and integration checkpoint, and [docs/ai-learning-log.md](docs/ai-learning-log.md) for the required genuine learning evidence.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

Run the full suite on the integrated `main` after feature merges. Record actual output only; do not infer a test count from an earlier run.
