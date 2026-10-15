"""Small, deterministic summary reports for CampusFlow."""


def generate_report(tickets: dict) -> dict:
    """Summarize ticket counts by status, priority, and category."""

    statuses = {"open": 0, "in_progress": 0, "resolved": 0}
    priorities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    categories = {}

    for ticket in tickets.values():
        status = ticket.get("status", "unknown")
        priority = ticket.get("priority", "unknown")
        category = ticket.get("category", "unknown")

        statuses[status] = statuses.get(status, 0) + 1
        priorities[priority] = priorities.get(priority, 0) + 1
        categories[category] = categories.get(category, 0) + 1

    open_count = statuses["open"]
    progress_count = statuses["in_progress"]
    unresolved = open_count + progress_count

    resolved_count = statuses["resolved"]
    total = len(tickets)

    if total == 0:
        resolution_percentage = 0
    else:
        resolution_percentage = (resolved_count / total) * 100

    return {
        "total": total,
        "by_status": statuses,
        "by_priority": priorities,
        "by_category": dict(sorted(categories.items())),
        "unresolved": unresolved,
        "resolved": resolved_count,
        "resolution_percentage": resolution_percentage,
    }