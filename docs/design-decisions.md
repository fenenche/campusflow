# Design decisions

## Separation of responsibilities
- `tickets.py` contains pure input validation, normalization, and priority calculation so these rules can be tested without terminal input or file I/O.
- `workflow.py` owns IDs, assignment, lifecycle transitions, and queue ordering.
- `storage.py` owns JSON input/output and reports clear errors for malformed or unexpected data.
- `reports.py` calculates summaries from the current ticket mapping.
- `main.py` handles prompts and display, delegating business logic to the modules above.

## Data model
Tickets are dictionaries keyed by their unique IDs (for example, `T001`). Each record contains `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, and `assigned_to`. A dictionary makes ID lookup and updates straightforward and serializes naturally to a JSON object.

## Priority
Rules are checked in the specified order so the combined high-urgency/large-impact case becomes `critical` before the broader `high` rule can match. Input strings are normalized to support case variations consistently.

## Lifecycle
New tickets start `open`. Only assigned tickets may transition to `in_progress`, and those tickets may transition to `resolved`. Resolved tickets may be reopened to `open`. Unsupported transitions raise `ValueError` instead of silently changing state.

## Persistence and IDs
A missing JSON file is treated as an empty store. Writes create parent directories. Invalid JSON and an unexpected top-level structure raise a useful `ValueError`. ID generation scans existing numeric `T` IDs and chooses the next number, preventing collisions after reload and avoiding reuse of a deleted lower ID.

## Queue and report
The open queue sorts by priority (`critical`, `high`, `medium`, `low`) and then numeric ticket ID. Reports provide total counts by status, priority, and category without changing ticket records.
