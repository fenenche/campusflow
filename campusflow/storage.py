"""Save and load Campusflow tickets as JSON."""

import json
from pathlib import Path
from typing import Any


def save_tickets(
    tickets: list[dict[str, Any]],
    filename: str | Path = "data/tickets.json",
) -> None:
    """Save tickets to a JSON file."""

    file_path = Path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(
    filename: str | Path = "data/tickets.json",
) -> list[dict[str, Any]]:
    """Load tickets from a JSON file."""

    file_path = Path(filename)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("The ticket storage file contains valid JSON.") from error

    if not isinstance(tickets, list):
        raise ValueError("The ticket storage file must contain a JSON array.")

    return tickets