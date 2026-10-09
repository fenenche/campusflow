"""Ticket lifecycle, assignment, ID generation, and priority queue."""

from .tickets import create_ticket

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
VALID_STATUSES = {"open", "in_progress", "resolved"}


def next_ticket_id(tickets: dict) -> str:
    """Generate the next TNNN ID without reusing an existing numeric ID."""
    largest = 0
    for key in tickets:
        if isinstance(key, str) and key.startswith("T") and key[1:].isdigit():
            largest = max(largest, int(key[1:]))
    candidate = largest + 1
    while f"T{candidate:03d}" in tickets:
        candidate += 1
    return f"T{candidate:03d}"


def add_ticket(tickets: dict, title: str, category: str, urgency: str, affected_users: int) -> dict:
    """Create and store a ticket in the supplied ticket mapping."""
    ticket_id = next_ticket_id(tickets)
    ticket = create_ticket(title, category, urgency, affected_users, ticket_id)
    tickets[ticket_id] = ticket
    return ticket


def _get_ticket(tickets: dict, ticket_id: str) -> dict:
    try:
        return tickets[ticket_id]
    except KeyError as exc:
        raise ValueError(f"Unknown ticket ID: {ticket_id}.") from exc


def assign_ticket(tickets: dict, ticket_id: str, staff_name: str) -> dict:
    """Assign a ticket to a non-empty staff name."""
    ticket = _get_ticket(tickets, ticket_id)
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name must not be blank.")
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def update_ticket_status(tickets: dict, ticket_id: str, new_status: str) -> dict:
    """Apply allowed status transitions; unassigned tickets cannot be started."""
    ticket = _get_ticket(tickets, ticket_id)
    if not isinstance(new_status, str) or new_status.strip().lower() not in VALID_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    new_status = new_status.strip().lower()
    current = ticket.get("status")
    allowed = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": {"open"},  # reopening is supported explicitly
    }
    if new_status == current:
        return ticket
    if new_status not in allowed.get(current, set()):
        raise ValueError(f"Invalid status transition: {current} -> {new_status}.")
    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Assign the ticket before moving it to in_progress.")
    ticket["status"] = new_status
    return ticket


def priority_queue(tickets: dict) -> list:
    """Return open tickets sorted by priority, then numeric ticket ID."""
    def numeric_id(ticket: dict) -> int:
        ticket_id = str(ticket.get("id", ""))
        suffix = ticket_id[1:] if ticket_id.startswith("T") else ""
        return int(suffix) if suffix.isdigit() else 10**12

    opened = [ticket for ticket in tickets.values() if ticket.get("status") == "open"]
    return sorted(opened, key=lambda t: (PRIORITY_ORDER.get(t.get("priority"), 99), numeric_id(t)))
