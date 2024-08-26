import Bank_Accounts as bk


def main():
    # Main loop to display the menu and process user selections
    try:
        while True:
            option: str = bk.print_menu();

            match option:
                case "1":
                    bk.add_transaction();
                case "2":
                    bk.execute_transactions(due_only=False);
                case "3":
                    bk.execute_transactions(due_only=True);
                case "4":
                    bk.reports_interface();
                case "5":
                    bk.open_new_account();
                case "6":
                    print("Exiting the system.");
                    break;
                case _:
                    print("Invalid option. Please try again.");

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.");


if __name__ == "__main__":
    main();