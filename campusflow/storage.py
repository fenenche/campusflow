"""JSON persistence for CampusFlow tickets."""

import json
from pathlib import Path


def save_tickets(tickets: dict, filename: str = "data/tickets.json") -> None:
    """Persist a mapping of ticket ID to ticket record, creating parent folders."""
    if not isinstance(tickets, dict):
        raise ValueError("Tickets must be a dictionary keyed by ticket ID.")
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(tickets, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def load_tickets(filename: str = "data/tickets.json") -> dict:
    """Load tickets; a missing file is an empty store, malformed JSON is an error."""
    path = Path(filename)
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            tickets = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError("Ticket storage contains invalid JSON.") from exc
    if not isinstance(tickets, dict):
        raise ValueError("Ticket storage must contain a JSON object keyed by ticket ID.")
    for ticket_id, ticket in tickets.items():
        if not isinstance(ticket_id, str) or not isinstance(ticket, dict):
            raise ValueError("Each stored ticket must be an object keyed by a string ID.")
        if ticket.get("id") != ticket_id:
            raise ValueError(f"Stored ticket key does not match ticket ID: {ticket_id}.")
    return tickets
