"""Case-insensitive ticket title search and composable filters."""

from __future__ import annotations

from typing import Any, Iterable

Ticket = dict[str, Any]
CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def _normalise_filter(value: str | None, allowed: tuple[str, ...], field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field.title()} filter must be text.")
    normalised = value.strip().casefold()
    allowed_normalised = {item.casefold() for item in allowed}
    if normalised not in allowed_normalised:
        raise ValueError(f"Invalid {field} filter: {value!r}.")
    return normalised


def search_tickets(
    tickets: Iterable[Ticket],
    title_query: str = "",
    category: str | None = None,
    status: str | None = None,
    priority: str | None = None,
) -> list[Ticket]:
    """Return matching tickets without mutating the source iterable.

    A title query is a case-insensitive substring. All supplied filters are
    conjunctive (AND semantics); empty title query and omitted filters impose
    no restriction.
    """
    if not isinstance(title_query, str):
        raise ValueError("Title search must be text.")

    category_filter = _normalise_filter(category, CATEGORIES, "category")
    status_filter = _normalise_filter(status, STATUSES, "status")
    priority_filter = _normalise_filter(priority, PRIORITIES, "priority")
    query = title_query.strip().casefold()

    matches: list[Ticket] = []
    for ticket in tickets:
        title = ticket.get("title", "")
        if not isinstance(title, str):
            continue
        if query not in title.casefold():
            continue
        if category_filter is not None and str(ticket.get("category", "")).casefold() != category_filter:
            continue
        if status_filter is not None and str(ticket.get("status", "")).casefold() != status_filter:
            continue
        if priority_filter is not None and str(ticket.get("priority", "")).casefold() != priority_filter:
            continue
        matches.append(ticket)
    return matches
