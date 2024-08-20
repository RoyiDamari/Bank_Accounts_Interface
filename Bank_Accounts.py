from datetime import datetime, date

# Sample initial data for three accounts
bank_accounts: dict[int, [str, any]] = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [("2024-08-17 14:00:00", "2024-08-18 14:00:00", 1001, 1002, 300),
                                    ("2024-08-17 15:00:00", "2024-08-19 15:00:00", 1001, 1003, 200)],
        "transaction_history": [("2024-08-15 09:00:00", "2024-08-15 09:30:00", 1001, 1002, 500, "2024-08-15 09:30:00")]
    },
    1002: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": 1500.00,
        "transactions_to_execute": [],
        "transaction_history": []
    },
    1003: {
        "first_name": "Charlie",
        "last_name": "Brown",
        "id_number": "555555555",
        "balance": 3500.75,
        "transactions_to_execute": [],
        "transaction_history": []
    }
};


def print_menu() -> str:
    print("\n--- Banking System Menu ---");
    print("1. Add a new transaction");
    print("2. Execute all pending transactions");
    print("3. Execute all due transactions");
    print("4. Reports interface");
    print("5. Open a new account");
    print("6. Exit");
    return input("Select an option (1-5): ");


def add_transaction() -> None:
    print("\n--- Add a New Transaction ---");
    # Get a valid source account number
    while True:
        try:
            source_account: int = int(input("Enter source account number: "));
            if source_account not in bank_accounts:
                raise ValueError("Source account number does not exist.");
            break;
        except ValueError as e:
            print(f"Invalid source account number: {e}. Please try again.");

    # Get a valid target account number
    while True:
        try:
            target_account: int = int(input("Enter target account number: "));
            if target_account not in bank_accounts:
                raise ValueError("Target account number does not exist.");
            break;
        except ValueError as e:
            print(f"Invalid target account number: {e}. Please try again.");

    # Get a valid amount
    while True:
        try:
            amount: float = float(input("Enter amount to transfer: "));
            if amount <= 0:
                raise ValueError("The amount must be a positive number.");
            if amount > bank_accounts[source_account]["balance"]:
                raise ValueError(f"The amount exceeds the available balance. "
                                 f"You can transfer up to {bank_accounts[source_account]['balance']}.");
            break;
        except ValueError as e:
            print(f"Invalid amount: {e}. Please enter a valid positive number.");

    # Get the current time for transaction creation
    creation_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");

    # Get a valid future transaction time
    while True:
        try:
            future_time: str = input("Enter the future time for execution (YYYY-MM-DD HH:MM:SS): ");
            future_datetime: datetime = datetime.strptime(future_time, "%Y-%m-%d %H:%M:%S");
            if future_datetime < datetime.now():
                raise ValueError("The time entered must be in the future.");
            break
        except ValueError as e:
            print(f"Invalid datetime format or past date: {e}. Please try again.");

    transaction: tuple[str, str, int, int, float] = (creation_time, future_time, source_account,
                                                     target_account, amount);
    bank_accounts[source_account]["transactions_to_execute"].append(transaction);
    print("Transaction added successfully.");


def execute_transactions(due_only: bool = False) -> None:
    while True:
        try:
            source_account: int = int(input("Enter the account number to execute transactions: "))
            if source_account not in bank_accounts:
                raise ValueError("Account number does not exist")
            break
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid account number.")

    transactions_to_execute: list[tuple[str, str, int, int, float]] = bank_accounts[source_account][
        "transactions_to_execute"]
    transaction_history: list[tuple[str, str, int, int, float, str]] = bank_accounts[source_account][
        "transaction_history"]

    executed_any: bool = False

    for transaction in transactions_to_execute[:]:
        creation_time, future_time_str, source, target, amount = transaction

        # If executing due transactions only, check if the future time has arrived
        if due_only:
            future_time = datetime.strptime(future_time_str, "%Y-%m-%d %H:%M:%S")
            if future_time > datetime.now():
                continue

        # Update balances
        bank_accounts[source]["balance"] -= amount
        bank_accounts[target]["balance"] += amount

        # Add the transaction to history with execution time
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        executed_transaction = transaction + (execution_time,)
        transaction_history.append(executed_transaction)

        # Remove the executed transaction from the pending list
        transactions_to_execute.remove(transaction)

        # Print each transaction as it's executed
        print(f"Executed transaction: {executed_transaction}")
        executed_any = True

    if not executed_any:
        print("No transactions were executed.")
    else:
        # Print account details after transactions are completed
        print_account_details(source_account)


def print_account_details(account_number: int) -> None:
    account: dict[str, any] = bank_accounts.get(account_number);
    if not account:
        print(f"No account found with account number {account_number}");
    else:
        print(f"\nAccount {account_number} details:");
        for key, value in account.items():
            print(f"{key}: {value}");


def reports_interface() -> None:
    while True:
        print("\n--- Reports Menu: ---");
        print("1. Print all bank accounts details");
        print("2. Print account details by account number");
        print("3. Print account details by ID");
        print("4. Print account details by first name");
        print("5. Print all accounts sorted by balance");
        print("6. Print all transaction history");
        print("7. Print today's transactions");
        print("8. Print accounts with negative balance");
        print("9. Print the sum of all account balances");
        print("10. Return to main menu");

        option_menu: str = input("Select an option (1-10): ");

        match option_menu:
            case "1":
                print("\nAll bank accounts:");
                for account_number in bank_accounts:
                    print_account_details(account_number);

            case "2":
                while True:
                    try:
                        account_number: int = int(input("Enter account number: "))
                        if account_number not in bank_accounts:
                            raise ValueError("Account number does not exist.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please enter a valid account number.")
                print_account_details(account_number);

            case "3":
                while True:
                    try:
                        id_number: str = input("Enter ID number: ");
                        found: bool = False;
                        for account_number, account in bank_accounts.items():
                            if account["id_number"] == id_number:
                                print_account_details(account_number);
                                found = True;
                        if not found:
                            raise ValueError("ID number does not exist.");
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please try again.");

            case "4":
                while True:
                    try:
                        first_name: str = input("Enter first name: ").lower();
                        found: bool = False;
                        for account_number, account in bank_accounts.items():
                            if first_name in account["first_name"].lower():
                                print_account_details(account_number);
                                found = True;
                        if not found:
                            raise ValueError("First name does not exist in any account.");
                        break;
                    except ValueError as e:
                        print(f"Error: {e}. Please try again.");
            case "5":
                sorted_accounts: list[tuple[int, dict[str, any]]] = sorted(bank_accounts.items(),
                                                                           key=lambda x: x[1]["balance"]);
                for account_number, account in sorted_accounts:
                    print_account_details(account_number);

            case "6":
                print("\nAll transaction history:");
                transactions: list[tuple[str, str, int, int, float, str]] = [];
                for account in bank_accounts.values():
                    transactions.extend(account["transaction_history"]);
                for transaction in sorted(transactions, key=lambda x: x[0], reverse=True):
                    print(transaction)

            case "7":
                today: str = date.today().strftime("%Y-%m-%d");
                transactions: list[tuple[str, str, int, int, float, str]] = [];
                print(f"\nTransactions for today ({today}):");
                for account in bank_accounts.values():
                    transactions.extend(account["transaction_history"]);
                for transaction in transactions:
                    if transaction[0].startswith(today):
                        print(transaction);

            case "8":
                print("\nAccounts with negative balance:");
                found_negative_balance: bool = False;
                for account_number, account in bank_accounts.items():
                    if account["balance"] < 0:
                        print_account_details(account_number);
                        found_negative_balance = True;
                if not found_negative_balance:
                    print("No account with negative balance was found.");

            case "9":
                total_balance: float = sum(account["balance"] for account in bank_accounts.values());
                print(f"\nTotal balance of all accounts: {total_balance}");

            case "10":
                print("Exiting the system.");
                break

            case _:
                print("Invalid option. Please try again.");


def open_new_account() -> None:
    print("\n--- Open a New Account ---");
    account_number: int = max(bank_accounts.keys()) + 1;
    first_name: str = input("Enter first name: ");
    last_name: str = input("Enter last name: ");
    id_number: str = input("Enter ID number: ");
    balance: float = float(input("Enter initial balance: "));

    bank_accounts[account_number] = {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "balance": balance,
        "transactions_to_execute": [],
        "transaction_history": []
    };
    print(f"New account created successfully with account number {account_number}.");

try:
    while True:
        option: str = print_menu()

        match option:
            case "1":
                add_transaction()
            case "2":
                execute_transactions(due_only=False)
            case "3":
                execute_transactions(due_only=True)
            case "4":
                reports_interface()
            case "5":
                open_new_account()
            case "6":
                print("Exiting the system.")
                break
            case _:
                print("Invalid option. Please try again.")

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting.")