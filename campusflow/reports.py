"""Aggregate ticket counts and resolution metrics for CampusFlow."""

from __future__ import annotations

from typing import Any, Iterable

Ticket = dict[str, Any]
_STATUSES = ("open", "in_progress", "resolved")
_PRIORITIES = ("critical", "high", "medium", "low")
_CATEGORIES = ("Network", "Hardware", "Software", "Other")


def generate_report(tickets: Iterable[Ticket]) -> dict[str, Any]:
    """Return total, status/priority/category counts and resolution metrics.

    All known values are represented, including zero counts. A ticket is
    unresolved when its current status is open or in_progress. Missing category
    is tolerated for legacy test/data records; unknown supplied categories fail.
    """
    status_counts = {status: 0 for status in _STATUSES}
    priority_counts = {priority: 0 for priority in _PRIORITIES}
    category_counts = {category: 0 for category in _CATEGORIES}
    total = 0

    for ticket in tickets:
        total += 1
        status = ticket.get("status")
        priority = ticket.get("priority")
        category = ticket.get("category")

        if status not in status_counts:
            raise ValueError(f"Unknown ticket status: {status!r}.")
        if priority not in priority_counts:
            raise ValueError(f"Unknown ticket priority: {priority!r}.")
        status_counts[status] += 1
        priority_counts[priority] += 1

        if category is not None:
            if not isinstance(category, str):
                raise ValueError(f"Unknown ticket category: {category!r}.")
            canonical = next(
                (item for item in _CATEGORIES if item.casefold() == category.casefold()),
                None,
            )
            if canonical is None:
                raise ValueError(f"Unknown ticket category: {category!r}.")
            category_counts[canonical] += 1

    resolved = status_counts["resolved"]
    unresolved = status_counts["open"] + status_counts["in_progress"]
    percentage = (resolved / total * 100.0) if total else 0.0

    return {
        "total": total,
        "by_status": status_counts,
        "by_priority": priority_counts,
        "by_category": category_counts,
        "resolution_percentage": percentage,
        "unresolved": unresolved,
        "unresolved_by_status": {
            "open": status_counts["open"],
            "in_progress": status_counts["in_progress"],
        },
    }
