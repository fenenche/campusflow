"""Interactive command-line interface for CampusFlow.

Business rules live in campusflow modules; this file handles user interaction,
display, persistence orchestration, and friendly error messages.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from campusflow.reports import generate_report
from campusflow.search import search_tickets
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import add_note, create_ticket, find_ticket
from campusflow.understanding_check import run_understanding_check
from campusflow.workflow import assign_ticket, change_status, get_open_queue, reopen_ticket

Ticket = dict[str, Any]
DEFAULT_DATA_FILE = Path("data/tickets.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CampusFlow ticket tracker")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_FILE,
                        help=f"path to the JSON ticket file (default: {DEFAULT_DATA_FILE})")
    return parser.parse_args()


def prompt_positive_integer(prompt: str) -> int:
    raw_value = input(prompt).strip()
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError("Enter a whole number, such as 1 or 12.") from exc
    if value <= 0:
        raise ValueError("Enter a number greater than zero.")
    return value


def print_ticket(ticket: Ticket) -> None:
    print("-" * 44)
    print(f"ID:             {ticket['id']}")
    print(f"Title:          {ticket['title']}")
    print(f"Category:       {ticket['category']}")
    print(f"Urgency:        {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority:       {ticket['priority'].upper()}")
    print(f"Status:         {ticket['status'].replace('_', ' ').title()}")
    print(f"Assigned to:    {ticket.get('assigned_to') or 'Unassigned'}")
    print("-" * 44)


def print_ticket_list(tickets: list[Ticket]) -> None:
    if not tickets:
        print("No tickets found.")
        return
    for ticket in sorted(tickets, key=lambda item: item["id"]):
        print_ticket(ticket)


def run_mutation(tickets: list[Ticket], data_path: Path, operation: Callable[[], Any]) -> Any | None:
    """Persist a mutation atomically from the CLI's point of view."""
    before = deepcopy(tickets)
    try:
        result = operation()
        save_tickets(data_path, tickets)
    except (ValueError, KeyError, StorageError) as exc:
        tickets[:] = before
        print(f"Error: {exc}")
        return None
    print(f"Saved to {data_path}.")
    return result


def create_ticket_menu(tickets: list[Ticket], data_path: Path) -> None:
    print("\nCreate a ticket")
    title = input("Title: ").strip()
    category = input("Category (Network/Hardware/Software/Other): ").strip()
    urgency = input("Urgency (low/medium/high): ").strip()
    try:
        affected_users = prompt_positive_integer("Number of affected users: ")
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    ticket = run_mutation(tickets, data_path, lambda: create_ticket(tickets, title, category, urgency, affected_users))
    if ticket is not None:
        print("Ticket created successfully.")
        print_ticket(ticket)


def view_ticket_menu(tickets: list[Ticket]) -> None:
    try:
        print_ticket(find_ticket(tickets, prompt_positive_integer("Ticket ID: ")))
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}")


def assign_ticket_menu(tickets: list[Ticket], data_path: Path) -> None:
    try:
        ticket_id = prompt_positive_integer("Ticket ID to assign: ")
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    staff_name = input("Staff member name: ").strip()
    ticket = run_mutation(tickets, data_path, lambda: assign_ticket(tickets, ticket_id, staff_name))
    if ticket is not None:
        print(f"Ticket #{ticket_id} assigned to {ticket['assigned_to']}.")


def change_status_menu(tickets: list[Ticket], data_path: Path) -> None:
    try:
        ticket_id = prompt_positive_integer("Ticket ID: ")
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    new_status = input("New status (in_progress/resolved): ").strip()
    ticket = run_mutation(tickets, data_path, lambda: change_status(tickets, ticket_id, new_status))
    if ticket is not None:
        print(f"Ticket #{ticket_id} is now {ticket['status']}.")


def reopen_ticket_menu(tickets: list[Ticket], data_path: Path) -> None:
    try:
        ticket_id = prompt_positive_integer("Ticket ID to reopen: ")
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    ticket = run_mutation(tickets, data_path, lambda: reopen_ticket(tickets, ticket_id))
    if ticket is not None:
        print(f"Ticket #{ticket_id} has been reopened.")


def show_open_queue(tickets: list[Ticket]) -> None:
    queue = get_open_queue(tickets)
    if not queue:
        print("The open queue is empty.")
        return
    print("\nOpen queue (highest priority first)")
    for ticket in queue:
        print(f"#{ticket['id']} [{ticket['priority'].upper()}] {ticket['title']} — {ticket['category']}")


def show_report(tickets: list[Ticket]) -> None:
    report = generate_report(tickets)
    print("\nCampusFlow report")
    print(f"Total tickets: {report['total']}")
    for heading, key in (("By status", "by_status"), ("By priority", "by_priority"), ("By category", "by_category")):
        print(f"\n{heading}:")
        for value, count in report[key].items():
            print(f"  {value.replace('_', ' ').title():<14} {count}")
    print(f"\nResolution percentage: {report['resolution_percentage']:.1f}%")
    print(f"Unresolved tickets: {report['unresolved']}")
    print(f"  Open: {report['unresolved_by_status']['open']}")
    print(f"  In progress: {report['unresolved_by_status']['in_progress']}")


def search_tickets_menu(tickets: list[Ticket]) -> None:
    print("\nSearch and filter tickets (leave fields blank to skip)")
    query = input("Title contains: ")
    category = input("Category (Network/Hardware/Software/Other): ").strip() or None
    status = input("Status (open/in_progress/resolved): ").strip() or None
    priority = input("Priority (critical/high/medium/low): ").strip() or None
    try:
        results = search_tickets(tickets, query, category, status, priority)
    except ValueError as exc:
        print(f"Error: {exc}")
        return
    print(f"Matching tickets: {len(results)}")
    print_ticket_list(results)


def manage_notes_menu(tickets: list[Ticket], data_path: Path) -> None:
    try:
        ticket_id = prompt_positive_integer("Ticket ID for notes: ")
        ticket = find_ticket(tickets, ticket_id)
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}")
        return
    action = input("Notes: (1) view, (2) add, (3) cancel: ").strip()
    if action == "1":
        notes = ticket.get("notes", [])
        if not notes:
            print("No notes for this ticket.")
            return
        for index, note in enumerate(notes, start=1):
            print(f"{index}. {note['author']}: {note['message']}")
    elif action == "2":
        author = input("Author: ")
        message = input("Message: ")
        run_mutation(tickets, data_path, lambda: add_note(tickets, ticket_id, author, message))
    elif action == "3":
        print("Cancelled.")
    else:
        print("Invalid notes action. Choose 1, 2, or 3.")


def print_menu() -> None:
    print(
        "\n=== CampusFlow ===\n"
        "1. Create ticket\n"
        "2. List all tickets\n"
        "3. View ticket by ID\n"
        "4. Assign ticket\n"
        "5. Change ticket status\n"
        "6. Reopen resolved ticket\n"
        "7. Show open queue\n"
        "8. Generate report\n"
        "9. Search and filter tickets\n"
        "10. View/add ticket notes\n"
        "11. Engineering Understanding Check\n"
        "12. Exit"
    )


def main() -> int:
    args = parse_args()
    try:
        tickets = load_tickets(args.data)
    except StorageError as exc:
        print(f"Startup error: {exc}")
        print("Fix or restore the data file, then run CampusFlow again.")
        return 1
    print(f"Loaded {len(tickets)} ticket(s) from {args.data}.")
    actions: dict[str, Callable[[], None]] = {
        "1": lambda: create_ticket_menu(tickets, args.data),
        "2": lambda: print_ticket_list(tickets),
        "3": lambda: view_ticket_menu(tickets),
        "4": lambda: assign_ticket_menu(tickets, args.data),
        "5": lambda: change_status_menu(tickets, args.data),
        "6": lambda: reopen_ticket_menu(tickets, args.data),
        "7": lambda: show_open_queue(tickets),
        "8": lambda: show_report(tickets),
        "9": lambda: search_tickets_menu(tickets),
        "10": lambda: manage_notes_menu(tickets, args.data),
        "11": lambda: run_understanding_check(),
    }
    while True:
        print_menu()
        choice = input("Choose an option (1-12): ").strip()
        if choice == "12":
            print("CampusFlow closed.")
            return 0
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Enter a number from 1 to 12.")
            continue
        try:
            action()
        except (ValueError, KeyError, StorageError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nCampusFlow closed.")
        raise SystemExit(0)