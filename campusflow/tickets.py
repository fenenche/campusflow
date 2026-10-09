"""Ticket creation, validation, and priority calculation."""

from typing import Any

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency: str, affected_users: int) -> str:
    """Calculate a ticket's priority from urgency and affected users."""

    if not isinstance(urgency, str) or urgency not in VALID_URGENCIES:
        raise ValueError(f"Invalid urgency: {urgency!r}")

    if (
        isinstance(affected_users, bool)
        or not isinstance(affected_users, int)
        or affected_users < 1
    ):
        raise ValueError("affected_users must be a positive integer.")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def validate_ticket_data(
    title: str,
    category: str,
    urgency: str,
    affected_users: int,
) -> None:
    """Validate the input fields required to create a ticket."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    if not isinstance(category, str) or category not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category: {category!r}. "
            f"Choose from {sorted(VALID_CATEGORIES)}."
        )

    calculate_priority(urgency, affected_users)


def create_ticket(
    title: str,
    category: str,
    urgency: str,
    affected_users: int,
    ticket_id: str,
) -> dict[str, Any]:
    """Create a validated ticket using an ID supplied by the caller."""

    validate_ticket_data(title, category, urgency, affected_users)

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID must be a non-empty string.")

    priority = calculate_priority(urgency, affected_users)

    return {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }