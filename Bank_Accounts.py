from datetime import datetime, date


# Function to initialize the bank accounts data structure
def init_interface() -> dict[int, dict[str, any]]:
    """
       Initializes the bank accounts data structure with some predefined accounts.

       Returns:
           dict[int, dict[str, any]]: A dictionary representing bank accounts,
           where the key is the account number and the value is another dictionary
           containing account details.
    """

    return {
        1001: {
            "first_name": "Alice",
            "last_name": "Smith",
            "id_number": "123456789",
            "balance": 2500.50,
            "transactions_to_execute": [
                ("2024-08-17 14:00:00", "2024-08-18 14:00:00", 1001, 1002, 300),
                ("2024-08-17 15:00:00", "2024-08-19 15:00:00", 1001, 1003, 200)
            ],
            "transaction_history": [
                ("2024-08-15 09:00:00", "2024-08-15 09:30:00", 1001, 1002, 500, "2024-08-15 09:30:00")
            ]
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


# Function to print the main menu and get user's selection
def print_menu() -> str:
    """
       Prints the main menu of the banking system and prompts the user for a selection.

       Returns:
           str: The user's selected menu option.
    """

    print("\n--- Banking System Menu ---");
    print("1. Add a new transaction");
    print("2. Execute all pending transactions");
    print("3. Execute all due transactions");
    print("4. Reports interface");
    print("5. Open a new account");
    print("6. Exit");
    return input("Select an option (1-6): ");


# Function to validate the account number
def account_validation_check(account_number: str, accounts: dict[int, dict[str, any]]) -> int | None:
    """
        Validates whether the provided account number exists in the accounts dictionary.

        Args:
            account_number (str): The account number provided by the user.
            accounts (dict): The dictionary containing all accounts.

        Returns:
            int | None: The validated account number or None if 'EX' is typed.

        Raises:
            ValueError: If the account number does not exist in the accounts.
    """

    if account_number.upper() == 'EX':
        return;
    account_number: int = int(account_number);
    if account_number not in accounts:
        raise ValueError("Source or target account number does not exist.");
    else:
        return account_number;


# Function to validate the amount to be transferred
def amount_validation_check(amount: str, account_number: int, accounts: dict[int, dict[str, any]]) -> float | None:
    """
        Validates the amount entered for a transaction to ensure it's positive and doesn't exceed the balance.

        Args:
            amount (str): The amount to be validated.
            account_number (int): The source account number.
            accounts (dict): The dictionary containing all accounts.

        Returns:
            float | None: The validated amount as a float or None if 'EX' is typed.

        Raises:
            ValueError: If the amount is not positive or exceeds the available balance.
    """

    if amount.upper() == 'EX':
        return;
    amount: float = float(amount);
    if amount <= 0:
        raise ValueError("The amount must be a positive number.");
    elif amount > accounts[account_number]["balance"]:
        raise ValueError(f"The amount exceeds the available balance. "
                         f"You can transfer up to {accounts[account_number]['balance']:.2f}.");
    else:
        return amount;


# Function to validate the date/time for future transactions
def date_validation_check(future_date: str) -> datetime | None:
    """
       Validates whether the provided future date is in the correct format and is in the future.

       Args:
           future_date (str): The date string to validate.

       Returns:
           datetime | None: The validated future datetime or None if 'EX' is typed.

       Raises:
           ValueError: If the date is not in the future or not in the correct format.
    """

    if future_date.upper() == 'EX':
        return;
    future_date: datetime = datetime.strptime(future_date, "%Y-%m-%d %H:%M:%S");
    if future_date < datetime.now():
        raise ValueError("The time entered must be in the future.");
    else:
        return future_date;


# Function to add a new transaction to the accounts
def add_transaction(accounts: dict[int, dict[str, any]]) -> dict[int, dict[str, any]]:
    """
       Adds a new transaction to the accounts' transaction queue.

       Args:
           accounts (dict): The dictionary containing all accounts.

       Returns:
           dict: The updated accounts dictionary after the transaction is added.
    """

    print("\n--- Add a New Transaction ---");

    while True:
        source_account: str = input("Enter source account number (or type 'EX' to return to the main menu): ");
        try:
            source_account_number: int | None = account_validation_check(source_account, accounts);
            if source_account_number is None:
                return accounts;
            break;
        except ValueError as e:
            print(f"Invalid source account number: {e} Please try again.");

    while True:
        target_account: str = input("Enter target account number (or type 'EX' to return to the main menu): ");
        try:
            target_account_number: int | None = account_validation_check(target_account, accounts);
            if target_account_number is None:
                return accounts;
            if target_account_number == source_account_number:
                print("The source and target account numbers cannot be the same. "
                      "Please enter a different target account number.");
                continue;
            break;
        except ValueError as e:
            print(f"Invalid target account number: {e} Please try again.");

    while True:
        amount_input: str = input("Enter amount to transfer (or type 'EX' to return to the main menu): ");
        try:
            amount: float | None = amount_validation_check(amount_input, source_account_number, accounts);
            if amount is None:
                return accounts;
            break;
        except ValueError as e:
            print(f"Invalid amount: {e} Please enter a valid positive number.");

    creation_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");

    while True:
        future_time: str = input("Enter the future time for execution (YYYY-MM-DD HH:MM:SS) "
                                 "or type 'EX' to return to the main menu: ");
        try:
            future_time: datetime | None = date_validation_check(future_time);
            if future_time is None:
                return accounts;
            future_datetime: str = future_time.strftime("%Y-%m-%d %H:%M:%S");
            break;
        except ValueError as e:
            print(f"Invalid datetime format or past date: {e}. Please try again.");

    transaction: tuple[str, str, int, int, float] = (creation_time, future_datetime, source_account_number,
                                                     target_account_number, amount);
    accounts[source_account_number]["transactions_to_execute"].append(transaction)
    print("Transaction added successfully.");
    return accounts;


# Function to execute pending or due transactions
def execute_transactions(accounts: dict[int, dict[str, any]], due_only: bool = False) -> dict[int, dict[str, any]]:
    """
       Executes transactions for a specific account, either all or only those due.

       Args:
           accounts (dict): The dictionary containing all accounts.
           due_only (bool): Whether to execute only transactions that are due (default is False).

       Returns:
           dict: The updated accounts dictionary after executing the transactions.
    """

    while True:
        source_account: str = input("Enter the account number to execute transactions "
                                    "(or type 'EX' to return to the main menu): ");
        try:
            source_account_number: int | None = account_validation_check(source_account, accounts);
            if source_account_number is None:
                return accounts;
            break;
        except ValueError as e:
            print(f"Error: {e} Please enter a valid account number.");

    transactions_to_execute: list[tuple[str, str, int, int, float]] = accounts[source_account_number][
        "transactions_to_execute"];
    transaction_history: list[tuple[str, str, int, int, float, str]] = accounts[source_account_number][
        "transaction_history"];

    executed_any: bool = False;

    for transaction in transactions_to_execute[:]:
        creation_time, future_time_str, source, target, amount = transaction;

        if due_only:
            future_time: datetime = datetime.strptime(future_time_str, "%Y-%m-%d %H:%M:%S");
            if future_time > datetime.now():
                continue;

        accounts[source]["balance"] -= amount;
        accounts[target]["balance"] += amount;

        execution_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
        executed_transaction: tuple[str, str, int, int, float, str] = transaction + (execution_time,)
        transaction_history.append(executed_transaction);

        transactions_to_execute.remove(transaction);

        print(f"Executed transaction: {executed_transaction}");
        executed_any = True;

    if not executed_any:
        print("No transactions were executed.");
    else:
        print_account_details(accounts, source_account_number);
    return accounts;


# Function to print account details
def print_account_details(accounts: dict[int, dict[str, any]], account_number: int) -> None:
    """
        Prints the details of a specific account.

        Args:
            accounts (dict): The dictionary containing all accounts.
            account_number (int): The account number to print details for.

        Returns:
            None
    """

    account: dict[str, any] = accounts.get(account_number);
    if not account:
        print(f"No account found with account number {account_number}.");
    else:
        print(f"\nAccount {account_number} details:");
        for key, value in account.items():
            if key == "balance":
                # Format the balance to always show two decimal places
                print(f"{key}: {value:.2f}");
            else:
                print(f"{key}: {value}");


# Function to handle various reports related to accounts
def reports_interface(accounts: dict[int, dict[str, any]]) -> None:
    """
        Provides an interface to generate various reports on bank accounts.

        Args:
            accounts (dict): The dictionary containing all accounts.

        Returns:
            None
    """

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
                for account_number in accounts:
                    print_account_details(accounts, account_number);

            case "2":
                while True:
                    account_number_input: str = input("Enter account number (or type 'EX' to return to the main menu): ")
                    try:
                        account_number: int | None = account_validation_check(account_number_input, accounts)
                        if account_number is None:
                            break;
                        print_account_details(accounts, account_number);
                        break;
                    except ValueError as e:
                        print(f"Error: {e} Please enter a valid account number.");

            case "3":
                while True:
                    id_number: str = input("Enter ID number (or type 'EX' to return to the main menu): ");
                    if id_number.upper() == 'EX':
                        break;
                    try:
                        found: bool = False;
                        for account_number, account in accounts.items():
                            if account["id_number"] == id_number:
                                print_account_details(accounts, account_number);
                                found = True;
                        if not found:
                            raise ValueError("ID number does not exist.");
                        break;
                    except ValueError as e:
                        print(f"Error: {e} Please try again.");
            case "4":
                while True:
                    first_name = input("Enter first name (or type 'EX' to return to the main menu): ").lower();
                    if first_name.upper() == 'EX':
                        break;
                    try:
                        found: bool = False;
                        for account_number, account in accounts.items():
                            if first_name in account["first_name"].lower():
                                print_account_details(accounts, account_number);
                                found = True;
                        if not found:
                            raise ValueError("First name does not exist in any account.");
                        break;
                    except ValueError as e:
                        print(f"Error: {e} Please try again.");

            case "5":
                for account_number, account in sorted(accounts.items(), key=lambda x: x[1]["balance"]):
                    print_account_details(accounts, account_number);

            case "6":
                print("\nAll transaction history:");
                transactions: list[tuple[str, str, int, int, float, str]] = [];
                for account in accounts.values():
                    transactions.extend(account["transaction_history"]);
                for transaction in sorted(transactions, key=lambda x: x[0], reverse=True):
                    print(transaction);

            case "7":
                today: str = date.today().strftime("%Y-%m-%d");
                transactions: list[tuple[str, str, int, int, float, str]] = [];
                print(f"\nTransactions for today ({today}):");
                for account in accounts.values():
                    transactions.extend(account["transaction_history"]);
                for transaction in transactions:
                    if transaction[0].startswith(today):
                        print(transaction);

            case "8":
                print("\nAccounts with negative balance:");
                found_negative_balance: bool = False;
                for account_number, account in accounts.items():
                    if account["balance"] < 0:
                        print_account_details(accounts, account_number);
                        found_negative_balance = True;
                if not found_negative_balance:
                    print("No account with negative balance was found.");

            case "9":
                total_balance: float = sum(account["balance"] for account in accounts.values());
                print(f"\nTotal balance of all accounts: {total_balance}");

            case "10":
                print("Returning to main menu.");
                break;

            case _:
                print("Invalid option. Please try again.");


# Function to open a new bank account
def open_new_account(accounts: dict[int, dict[str, any]]) -> dict[int, dict[str, any]]:
    """
       Opens a new bank account by collecting user input for account details.

       Args:
           accounts (dict): The dictionary containing all accounts.

       Returns:
           dict: The updated accounts dictionary after the new account is added.
    """

    print("\n--- Open a New Account ---");
    account_number: int = max(accounts.keys()) + 1;

    while True:
        try:
            first_name: str = input("Enter first name (or type 'EX' to return to the main menu): ");
            if first_name.upper() == 'EX':
                return accounts;
            if not first_name.isalpha():
                raise ValueError("First name should only contain letters.");
            break;  # Exit the loop if the input is valid
        except ValueError as e:
            print(f"Error: {e}. Please enter valid information and try again.");

    while True:
        try:
            last_name: str = input("Enter last name (or type 'EX' to return to the main menu): ");
            if last_name.upper() == 'EX':
                return accounts;
            if not last_name.isalpha():
                raise ValueError("Last name should only contain letters.");
            break;  # Exit the loop if the input is valid
        except ValueError as e:
            print(f"Error: {e}. Please enter valid information and try again.");

    while True:
        try:
            id_number: str = input("Enter ID number (or type 'EX' to return to the main menu): ");
            if id_number.upper() == 'EX':
                return accounts;
            if not id_number.isdigit():
                raise ValueError("ID number should only contain digits.");
            break;  # Exit the loop if the input is valid
        except ValueError as e:
            print(f"Error: {e}. Please enter valid information and try again.");

    while True:
        try:
            balance = input("Enter initial balance (or type 'EX' to return to the main menu): ");
            if balance.upper() == 'EX':
                return accounts;
            balance = float(balance);
            if balance < 0:
                raise ValueError("Initial balance cannot be negative.");
            break;  # Exit the loop if the input is valid
        except ValueError as e:
            print(f"Error: {e}. Please enter valid information and try again.");

    accounts[account_number] = {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "balance": balance,
        "transactions_to_execute": [],
        "transaction_history": []
    }
    print(f"New account created successfully with account number {account_number}.");
    return accounts;
