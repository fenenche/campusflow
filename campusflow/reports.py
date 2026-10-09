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
    return {
        "total": len(tickets),
        "by_status": statuses,
        "by_priority": priorities,
        "by_category": dict(sorted(categories.items())),
    }
