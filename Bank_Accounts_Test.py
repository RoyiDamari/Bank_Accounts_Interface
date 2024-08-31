import Bank_Accounts as bk
import pytest
from datetime import datetime, timedelta
import time
import sys
from io import StringIO
import unittest
from unittest.mock import patch, call


# Tests for account_validation_check function


def test_account_validation_check_valid():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    expected: int = 123;

    # Act
    actual: int = bk.account_validation_check("123", accounts);

    # Assert
    assert actual == expected;


def test_account_validation_check_invalid():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};

    with pytest.raises(ValueError) as ex:
        bk.account_validation_check("999", accounts);

    # Assert
    assert str(ex.value) == "Source or target account number does not exist.";


def test_account_validation_check_non_numeric():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};

    with pytest.raises(ValueError) as ex:
        bk.account_validation_check("abc", accounts);


def test_account_validation_check_exit():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    expected: any = None;

    # Act
    actual: any = bk.account_validation_check("ex", accounts);

    # Assert
    assert actual == expected;


# Tests for amount_validation_check function


def test_amount_validation_check_valid():
    # Arrange
    amount: str = "100";
    account_number: int = 123;
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    expected: float = 100;

    # Act
    actual: float = bk.amount_validation_check(amount, account_number, accounts);

    # Assert
    assert actual == expected;


def test_amount_validation_check_invalid_non_numeric():
    # Arrange
    amount: str = "abc";
    account_number: int = 123;
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};

    with pytest.raises(ValueError) as ex:
        bk.amount_validation_check(amount, account_number, accounts);


def test_amount_validation_check_invalid_negative():
    # Arrange
    amount: str = "-500";
    account_number: int = 123;
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};

    with pytest.raises(ValueError) as ex:
        bk.amount_validation_check(amount, account_number, accounts);

    # Assert
    assert str(ex.value) == "The amount must be a positive number.";


def test_amount_validation_check_invalid_exceeds_balance():
    # Arrange
    amount: str = "2000";
    account_number: int = 123;
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};

    with pytest.raises(ValueError) as ex:
        bk.amount_validation_check(amount, account_number, accounts);

    # Assert
    assert str(ex.value) == "The amount exceeds the available balance. You can transfer up to 1500.00.";


def test_amount_validation_check_exit():
    # Arrange
    amount: str = "ex";
    account_number: int = 123;
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    expected: any = None;

    # Act
    actual: any = bk.amount_validation_check(amount, account_number, accounts);

    # Assert
    assert actual == expected;


# Tests for date_validation_check function


def test_date_validation_check_valid():
    # Arrange
    date: str = "2025-08-28 10:05:20";
    expected: datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S");

    # Act
    actual: datetime = bk.date_validation_check(date);

    # Assert
    assert actual == expected;


def test_date_validation_check_invalid_format():
    # Arrange
    date: str = "28-08-2024 10:05:20";

    with pytest.raises(ValueError) as ex:
        bk.date_validation_check(date);


def test_date_validation_check_nonexistent_date():
    # Arrange
    date: str = "2024-02-30 10:05:20";

    with pytest.raises(ValueError) as ex:
        bk.date_validation_check(date);


def test_date_validation_check_empty_string():
    # Arrange
    date: str = "";

    with pytest.raises(ValueError) as ex:
        bk.date_validation_check(date);


def test_date_validation_check_invalid():
    date: str = "2024-08-20 10:05:20";

    with pytest.raises(ValueError) as ex:
        bk.date_validation_check(date);

    # Assert
    assert str(ex.value) == "The time entered must be in the future.";


def test_date_validation_check_exit():
    # Arrange
    date: str = "ex";
    expected: any = None;

    # Act
    actual: any = bk.date_validation_check(date);

    # Assert
    assert actual == expected;


# Tests for add_transaction function


def test_add_transaction_to_existing_account():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
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

    # Mock inputs
    transaction_input: list[str] = [
        "1002",  # Source account
        "1003",  # Target account
        "100",  # Amount to transfer
        "2024-12-31 23:59:59"  # Future time for execution
    ];

    expected_creation_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S");

    expected: tuple[str, str, int, int, float] = (
        expected_creation_time,
        "2024-12-31 23:59:59",
        1002,
        1003,
        100.00
    );

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.add_transaction(accounts);

    # Assert
    assert accounts[1002]["transactions_to_execute"] == [expected];


def test_add_transaction_exit_on_source_account():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
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

    transaction_input: list[str] = ["EX"]; # Simulate the user typing "EX" to exit

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.add_transaction(accounts);

    # Assert
    assert accounts[1002]["transactions_to_execute"] == [];


def test_add_transaction_after_multiple_invalid_inputs():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
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

    transaction_input: list[str] = [
        "999",  # Invalid source account
        "1002",  # Valid source account
        "999",  # Invalid target account
        "1002",  # Source and target account are same
        "1003",  # Target account
        "-50",  # Invalid amount (negative)
        "2000",  # Invalid amount (exceeds the balance)
        "100",  # Valid amount after retry
        "2020-01-01 00:00:00",  # Invalid past date
        "2024-12-31 23:59:59"  # Valid future date after retry
    ];

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.add_transaction(accounts);

    expected_creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expected: tuple[str, str, int, int, float] = (
        expected_creation_time,
        "2024-12-31 23:59:59",
        1002,
        1003,
        100.00
    );

    assert accounts[1002]["transactions_to_execute"] == [expected];


# Tests for execute_transactions function


def test_execute_transactions_basic_execution():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 1500.00,
            "transactions_to_execute": [("2024-08-01 12:00:00", "2024-08-30 12:00:00", 1002, 1003, 100.00)],
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

    transaction_input: list[str] = ["1002", "EX"];

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.execute_transactions(accounts);

    # Assert
    assert accounts[1002]["balance"] == 1400.00;
    assert accounts[1003]["balance"] == 3600.75;
    assert len(accounts[1002]["transaction_history"]) == 1;
    assert accounts[1002]["transactions_to_execute"] == [];


def test_execute_transactions_due_only():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 1500.00,
            "transactions_to_execute": [("2024-08-01 12:00:00", "2024-11-20 12:00:00", 1002, 1003, 100.00)],
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

    transaction_input: list[str] = ["1002", "EX"];

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.execute_transactions(accounts, due_only=True);

    # Assert
    assert accounts[1002]["balance"] == 1500.00;  # Balance should remain the same
    assert accounts[1003]["balance"] == 3500.75;  # Balance should remain the same
    assert len(accounts[1002]["transaction_history"]) == 0;  # No transactions should be executed
    assert len(accounts[1002]["transactions_to_execute"]) == 1;  # Transaction should remain in queue


def test_execute_transactions_invalid_account_number_no_transactions_to_execute():
    # Arrange
    accounts: dict[int, dict[str, any]] = {
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

    transaction_input: list[str] = ["9999", "1002", "EX"];  # First invalid account, then valid

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.execute_transactions(accounts);

    # Assert
    # No changes should be made to the account since no transactions were present
    assert accounts[1002]["balance"] == 1500.00;
    assert accounts[1002]["transactions_to_execute"] == [];
    assert len(accounts[1002]["transaction_history"]) == 0;


def test_execute_transactions_future_transactions_due():
    # Arrange
    future_time: str = (datetime.now() + timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S");
    accounts: dict[int, dict[str, any]] = {
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 1500.00,
            "transactions_to_execute": [(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), future_time, 1002, 1003, 100.00)],
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

    transaction_input: list[str] = ["1002", "EX"];

    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.execute_transactions(accounts, due_only=True);

    # Assert
    # Wait for the future time to pass
    time.sleep(1.5);

    # Execute the transactions again, now they should be due
    with patch('builtins.input', side_effect=transaction_input):
        accounts: dict[int, dict[str, any]] = bk.execute_transactions(accounts, due_only=True);

    assert accounts[1002]["balance"] == 1400.00;
    assert accounts[1003]["balance"] == 3600.75;
    assert len(accounts[1002]["transaction_history"]) == 1;
    assert accounts[1002]["transactions_to_execute"] == [];


# Tests for print_account_details function


def test_print_account_details_non_existing_account():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": 1500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    non_existing_account: int = 999;
    expected: str = "No account found with account number 999.\n";

    # Act
    # Redirect stdout to capture prints
    actual: StringIO = StringIO();
    sys.stdout = actual;

    bk.print_account_details(accounts, non_existing_account);

    # Reset redirect.
    sys.stdout = sys.__stdout__;

    # Assert
    assert actual.getvalue() == expected;


def test_print_account_details_negative_balance():
    # Arrange
    accounts: dict[int, dict[str, any]] = {123: {"first_name": "Bob", "last_name": "Johnson", "id_number": "987654321",
                                                 "balance": -500.00, "transactions_to_execute": [],
                                                 "transaction_history": []}};
    expected: str = "\nAccount 123 details:\n" \
                    "first_name: Bob\n" \
                    "last_name: Johnson\n" \
                    "id_number: 987654321\n" \
                    "balance: -500.00\n" \
                    "transactions_to_execute: []\n" \
                    "transaction_history: []\n";

    # Act
    # Redirect stdout to capture prints
    actual: StringIO = StringIO();
    sys.stdout = actual;

    bk.print_account_details(accounts, 123);

    # Reset redirect.
    sys.stdout = sys.__stdout__;

    # Assert
    assert actual.getvalue() == expected;


# Tests for reports_interface function


def create_mock_accounts():
    return {
        1001: {
            "first_name": "Alice",
            "last_name": "Smith",
            "id_number": "123456789",
            "balance": 2500.00,
            "transactions_to_execute": [],
            "transaction_history": [
                ("2024-08-01 10:00:00", "2024-08-01 10:00:00", 1001, 1002, 100.00, "2024-08-01 10:00:01")
            ]
        },
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 1500.00,
            "transactions_to_execute": [],
            "transaction_history": []
        }
    };


@patch('builtins.input', side_effect=["1", "10"])
@patch('builtins.print')
def test_print_all_bank_accounts_details(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that the menu was printed
    assert mock_print.called;
    assert call("\n--- Reports Menu: ---") in mock_print.call_args_list;
    assert call("1. Print all bank accounts details") in mock_print.call_args_list;

    # Check that "All bank accounts:" was printed
    assert call("\nAll bank accounts:") in mock_print.call_args_list;

    # Ensure the account details were printed
    assert any("Alice" in str(c) for c in mock_print.call_args_list);
    assert any("Bob" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["2", "1001", "EX", "10"])
@patch('builtins.print')
def test_print_account_details_by_account_number(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    with patch('Bank_Accounts.account_validation_check', return_value=1001):
        bk.reports_interface(accounts);

    # Check that the specific account details were printed
    assert any("Alice" in str(c) for c in mock_print.call_args_list);
    assert any("Smith" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["3", "123456789", "EX", "10"])
@patch('builtins.print')
def test_print_account_details_by_id(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that the specific account details were printed by ID
    assert any("Alice" in str(c) for c in mock_print.call_args_list);
    assert any("Smith" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["4", "Alice", "EX", "10"])
@patch('builtins.print')
def test_print_account_details_by_first_name(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that the specific account details were printed by first name
    assert any("Alice" in str(c) for c in mock_print.call_args_list);
    assert any("Smith" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["5", "10"])
@patch('builtins.print')
def test_print_all_accounts_sorted_by_balance(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Debugging: print out what was actually printed
    # Extract the actual print calls for debugging

    print_calls = [str(printed_call[0][0]) for printed_call in mock_print.call_args_list]

    # Check that "Account 1002 details:" appears before "Account 1001 details:"
    account_1002_index = None
    account_1001_index = None

    for i, c in enumerate(print_calls):
        if "Account 1002 details:" in c:
            account_1002_index = i
        if "Account 1001 details:" in c:
            account_1001_index = i

    # Ensure both were found and in the correct order
    assert account_1002_index is not None;
    assert account_1001_index is not None;
    assert account_1002_index < account_1001_index;


@patch('builtins.input', side_effect=["6", "10"])
@patch('builtins.print')
def test_print_all_transaction_history(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that transaction history was printed
    assert any("2024-08-01 10:00:00" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["7", "10"])
@patch('builtins.print')
def test_print_today_transactions(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    with patch('Bank_Accounts.date', wraps=datetime) as mock_date:
        mock_date.today.return_value = datetime.strptime("2024-08-01", "%Y-%m-%d")
        bk.reports_interface(accounts);

    # Extract the relevant print calls
    print_calls = [str(printed_call[0][0]) for printed_call in mock_print.call_args_list];

    # Check that today's transactions were printed
    assert any("2024-08-01" in str(c) for c in mock_print.call_args_list);

    # Extract only the transaction-related print statements
    today_transactions = [c for c in print_calls if "2024-08-01" in c];

    # Check if the transactions are in reverse chronological order
    # Assuming transactions are in the format: ('2024-08-01 14:00:00', source_account, target_account, amount, ...)
    transaction_timestamps = [c.split()[0] for c in today_transactions]  # Extracting the timestamps

    # Make sure the list is sorted in reverse order
    assert transaction_timestamps == sorted(transaction_timestamps, reverse=True)


@patch('builtins.input', side_effect=["8", "10"])
@patch('builtins.print')
def test_print_accounts_with_negative_balance(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    accounts[1002]["balance"] = -50.00;
    bk.reports_interface(accounts);

    # Check that accounts with negative balance were printed
    assert any("Bob" in str(c) for c in mock_print.call_args_list);
    assert any("-50.0" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["9", "10"])
@patch('builtins.print')
def test_print_sum_of_all_account_balances(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that the sum of all balances was printed
    assert any("4000.0" in str(c) for c in mock_print.call_args_list);


@patch('builtins.input', side_effect=["10"])
@patch('builtins.print')
def test_return_to_main_menu(mock_print, mock_input):
    accounts: dict[int, dict[str, any]] = create_mock_accounts();
    bk.reports_interface(accounts);

    # Check that the function correctly indicates a return to the main menu
    assert any("Returning to main menu." in str(c) for c in mock_print.call_args_list);


# Tests for open_new_account function

def create_new_mock_accounts():
    return {
        1001: {
            "first_name": "Alice",
            "last_name": "Smith",
            "id_number": "123456789",
            "balance": 2500.00,
            "transactions_to_execute": [],
            "transaction_history": []
        },
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 1500.00,
            "transactions_to_execute": [],
            "transaction_history": []
        }
    };


@patch('builtins.input', side_effect=["John", "Doe", "123456789", "1000.00"])
def test_open_new_account_valid_input(mock_input):
    accounts: dict[int, dict[str, any]] = create_new_mock_accounts();
    updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

    # Check that the new account was created
    assert 1003 in updated_accounts;
    assert updated_accounts[1003]['first_name'] == "John";
    assert updated_accounts[1003]['last_name'] == "Doe";
    assert updated_accounts[1003]['id_number'] == "123456789";
    assert updated_accounts[1003]['balance'] == 1000.00;


@patch('builtins.input', side_effect=["John123", "John", "Doe", "123456789", "1000.00"])
def test_open_new_account_invalid_first_name_then_valid(mock_input):
    accounts: dict[int, dict[str, any]] = create_new_mock_accounts();
    updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

    # Check that the new account was created after correcting first name
    assert 1003 in updated_accounts;
    assert updated_accounts[1003]['first_name'] == "John";


@patch('builtins.input', side_effect=["John", "Doe123", "Doe", "123456789", "1000.00"])
def test_open_new_account_invalid_last_name_then_valid(mock_input):
    accounts: dict[int, dict[str, any]] = create_new_mock_accounts();
    updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

    # Check that the new account was created after correcting last name
    assert 1003 in updated_accounts;
    assert updated_accounts[1003]['last_name'] == "Doe";


@patch('builtins.input', side_effect=["John", "Doe", "ID123", "123456789", "1000.00"])
def test_open_new_account_invalid_id_number_then_valid(mock_input):
    accounts: dict[int, dict[str, any]] = create_new_mock_accounts();
    updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

    # Check that the new account was created after correcting ID number
    assert 1003 in updated_accounts;
    assert updated_accounts[1003]['id_number'] == "123456789";


@patch('builtins.input', side_effect=["John", "Doe", "123456789", "-1000.00", "1000.00"])
def test_open_new_account_invalid_balance_then_valid(mock_input):
    accounts: dict[int, dict[str, any]] = create_new_mock_accounts();
    updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

    # Check that the new account was created after correcting the balance
    assert 1003 in updated_accounts;
    assert updated_accounts[1003]['balance'] == 1000.00;


@patch('builtins.input', side_effect=[
    "EX",                         # Exit on first name
    "John", "EX",                 # Exit on last name
    "John", "Doe", "EX",          # Exit on ID number
    "John", "Doe", "123456789", "EX"  # Exit on balance
])
def test_open_new_account_exit_scenarios(mock_input):
    # Loop over the different scenarios, resetting accounts each time
    for _ in range(4):  # We have 4 scenarios
        accounts: dict[int, dict[str, any]] = create_new_mock_accounts(); # Reset the accounts dictionary before each test
        updated_accounts: dict[int, dict[str, any]] = bk.open_new_account(accounts);

        # Ensure no new account is created
        assert 1003 not in updated_accounts;


if __name__ == '__main__':
    unittest.main()
