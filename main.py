"""Interactive command-line interface for CampusFlow."""

from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import add_ticket, assign_ticket, update_ticket_status, priority_queue
from campusflow.reports import generate_report

DATA_FILE = "data/tickets.json"


def _print_ticket(ticket: dict) -> None:
    print(
        f'{ticket["id"]} | {ticket["title"]} | {ticket["category"]} | '
        f'{ticket["urgency"]} | {ticket["affected_users"]} affected | '
        f'{ticket["priority"]} | {ticket["status"]} | '
        f'assigned: {ticket["assigned_to"] or "unassigned"}'
    )


def main() -> None:
    try:
        tickets = load_tickets(DATA_FILE)
    except ValueError as exc:
        print(f"Could not load ticket data: {exc}")
        return

    actions = {
        "1": "Create ticket", "2": "View all tickets", "3": "Assign ticket",
        "4": "Update ticket status", "5": "View priority queue",
        "6": "Generate report", "0": "Exit",
    }
    while True:
        print("\nCampusFlow Helpdesk")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save_tickets(tickets, DATA_FILE)
            print("Tickets saved. Goodbye!")
            return
        try:
            if choice == "1":
                title = input("Title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                affected = int(input("Affected users (positive integer): ").strip())
                ticket = add_ticket(tickets, title, category, urgency, affected)
                save_tickets(tickets, DATA_FILE)
                print("Created ticket:")
                _print_ticket(ticket)
            elif choice == "2":
                if not tickets:
                    print("No tickets yet.")
                for ticket in sorted(tickets.values(), key=lambda t: t["id"]):
                    _print_ticket(ticket)
            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip()
                staff = input("Staff member name: ")
                _print_ticket(assign_ticket(tickets, ticket_id, staff))
                save_tickets(tickets, DATA_FILE)
            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip()
                status = input("New status (open/in_progress/resolved): ").strip()
                _print_ticket(update_ticket_status(tickets, ticket_id, status))
                save_tickets(tickets, DATA_FILE)
            elif choice == "5":
                queue = priority_queue(tickets)
                if not queue:
                    print("No open tickets.")
                for ticket in queue:
                    _print_ticket(ticket)
            elif choice == "6":
                report = generate_report(tickets)
                print(f'Total tickets: {report["total"]}')
                for section in ("by_status", "by_priority", "by_category"):
                    print(f"{section.replace('_', ' ').title()}:")
                    for label, count in report[section].items():
                        print(f"  {label}: {count}")
            else:
                print("Unknown option. Choose a listed number.")
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
