import Bank_Accounts as bk


def main() -> None:
    # Main loop to display the menu and process user selections
    accounts = bk.init_interface();

    try:
        while True:
            option: str = bk.print_menu();

            match option:
                case "1":
                    accounts = bk.add_transaction(accounts);
                case "2":
                    accounts = bk.execute_transactions(accounts, due_only=False);
                case "3":
                    accounts = bk.execute_transactions(accounts, due_only=True);
                case "4":
                    bk.reports_interface(accounts);
                case "5":
                    accounts = bk.open_new_account(accounts);
                case "6":
                    print("Exiting the system.");
                    break;
                case _:
                    print("Invalid option. Please try again.");

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.");


if __name__ == "__main__":
    main();
