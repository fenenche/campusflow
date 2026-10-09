def display_menu():
    print("\n===== CAMPUSFLOW HELP DESK =====")
    print("1. Create ticket")
    print("2. View all tickets")
    print("3. Assign ticket")
    print("4. Update ticket status")
    print("5. View priority queue")
    print("6. Generate report")
    print("0. Exit")


def main():
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            print("Create ticket selected.")
        elif choice == "2":
            print("View all tickets selected.")
        elif choice == "3":
            print("Assign ticket selected.")
        elif choice == "4":
            print("Update ticket status selected.")
        elif choice == "5":
            print("View priority queue selected.")
        elif choice == "6":
            print("Generate report selected.")
        elif choice == "0":
            print("Thank you for using CampusFlow!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()