#!/usr/bin/env python3
"""Interact with a simulated bank teller system

This program allows the user to view and modify bank account
information for the various accounts of pre-defined customers,
as well as ones added during runtime."""

import argparse
import lib.menu as menu
import lib.account as account
import lib.retirement as retirement
import lib.checking as checking
import lib.customer as customer
import lib.savings as savings
import lib.money_market_fund as market_fund


def create_main_menu():
    """Creates the main menu for the teller program

    Returns a tuple of a menu object with the program's allowable
    menu selections, a dictionary with keys and values of the
    menu options, and a reversed dictionary of the same pairings."""
    main_menu = menu.Menu()
    menu_dict = {}
    menu_dict_rev = {}
    menu_options = [
        "Get Users",
        "New User",
        "Select User",
        "Display Accounts",
        "Withdraw",
        "Deposit",
        "New Account",
        "Quit",
    ]
    for idx, selection in enumerate(menu_options, 1):
        main_menu.add_selection(selection)
        menu_dict.update({selection: str(idx)})
        menu_dict_rev.update({str(idx): selection})
    return (main_menu, menu_dict, menu_dict_rev)


def get_input(quit_string=None, quit_idx=None):
    """Returns sanitized user input or -1 if program should exit

    Keyword arguments:
    quit_string -- word to quit program on
    quit_idx -- numerical index into main menu of the quit button

    At least quit_string must be passed as an argument,
    otherwise quit button functionality will not be performed.
    Returns sanitized user input or -1 if the program should
    perform either 'go-back' or a 'quit'."""
    while True:
        try:
            selection = input("> ")
            selection = selection.title().strip()
            if not selection:
                continue
            if quit_string:
                if selection == quit_string or selection == str(quit_idx):
                    return -1
            break

        except (KeyboardInterrupt, EOFError) as e:
            return -1

    return selection


def generate_default_users(users_list):
    """Manually generates the two required default users"""
    # TODO: Refactor to be more DRY
    user1 = customer.Customer("Sherri", "Perrson", 83)
    savings1 = savings.Savings(14356.99)
    checking1 = checking.Checking(1504.32)
    retirement1 = retirement.Retirement(43265.00)
    market_fund1 = market_fund.MoneyMarket(3560.75)
    user1.add_account("Savings", savings1)
    user1.add_account("Checking", checking1)
    user1.add_account("401K", retirement1)
    user1.add_account("Money Market Fund", market_fund1)

    user2 = customer.Customer("John", "Doe", 24)
    savings2 = savings.Savings(25.42)
    user2.add_account("Savings", savings1)

    users_list.append(user1)
    users_list.append(user2)
    return users_list


def get_users(users_list):
    "Returns a formatted string of all users and their IDs"
    legend = "(Last), (First) : (User_id)"
    final_list = [legend, "-" * len(legend)]
    for user in users_list:
        final_list.append(
            (f"{user.last_name}, " f"{user.first_name} : {user.user_id}")
        )
    return "\n".join(final_list)


def get_account_printout(selected_user):
    """Returns a formatted string of a customer's account statement"""
    f_name = selected_user.first_name
    l_name = selected_user.last_name
    account_title = f"{f_name} {l_name}'s Accounts"
    printout = "".join(
        (
            "\n",
            account_title,
            "\n",
            "-" * len(account_title),
            "\n",
            selected_user.get_all_balances(),
            "\n",
        )
    )
    return printout


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secret", choices=("backdoor",), default="")
    args = parser.parse_args()
    return args


def perform_transaction(account_type, number, amount, user, user_func):
    """Calls the passed transaction function after input validation

    Keyword arguments:
    account_type -- type of account to check against below tuple
    number -- account number of given type
    amount -- amount to withdraw or deposit
    user -- the Customer whose account is being modified
    user_func -- the function (withdraw/deposit) to perform

    Performs the validation of the first three arguments to ensure
    the passed function call is safe. Returns -4 for transactional
    error, -3 for invalid account type, -2 for number or amount
    unable to be converted to the correct data type, -1 for
    negative values, 0 for invalid index, and 1 for success.
    Also returns an informative string detailing the transaction
    details if relevant."""
    account_types = ("Checking", "Savings", "Money Market Fund", "401K")
    if account_type not in account_types:
        # Case: invalid account type
        return -3

    return_msg = {
        "Checking": {-1: "overdraft limit exceeded", 0: "account overdrafted"},
        "Savings": {-1: "account balance exceeded"},
        "401K": {
            -2: "not old enough to withdraw",
            -1: "account balance exceeded",
        },
        "Money Market Fund": {
            -2: "max monthly withdrawls: 2",
            -1: "account balance exceeded",
        },
    }
    info_msg = None

    try:
        number = int(number) - 1  # Index is number - 1
        amount = float(amount)
    except (TypeError, ValueError):
        # Case: unable to convert number/amount to int or float
        return (-2, None)
    if amount < 0 or number < 0:
        # Case: negative withdrawl/deposit amount
        return (-1, None)
    try:
        if account_type == "401K" and user_func == user.withdraw_from:
            rc = user_func(account_type, number, amount, user.age)
        else:
            rc = user_func(account_type, number, amount)

        if rc < 1:
            info_msg = return_msg[account_type][rc]
        if rc == 1:
            return (1, None)
        return (-4, info_msg) if info_msg else (1, info_msg)

    except IndexError:
        return (0, None)


def secret_print(users):
    for user in users:
        print(
            f"{user.first_name} {user.last_name}\n",
            f"Age: {user.age} User_id: {user.user_id}\n",
            get_account_printout(user),
        )


def select_user(users):
    """Returns selected user, 0 if invalid option or -1 for "go-back"

    Keyword arguments:
    users -- list of all users in customer databse

    Returns selected user, 0 should the program produce an error,
    and -1 for 'go-back'"""
    user_input = get_input("B")
    if user_input == -1:
        return -1
    try:
        user_input = int(user_input)
    except ValueError:
        return 0
    if 0 < user_input <= len(users):
        selected_user = users[user_input - 1]
        return selected_user
    else:
        return 0


def use_teller(opt):
    """Primary loop for the program"""
    # TODO: better docstring
    main_menu, menu_dict, menu_dict_rev = create_main_menu()
    users = []
    users = generate_default_users(users)
    selected_user = None
    account_types = ("Checking", "Savings", "Money Market Fund", "401K")
    default_error = "No active user account, "
    back_to_menu = "returning to main menu.\n"

    if opt.secret == "backdoor":
        secret_print(users)

    while True:
        default_error = "No active user account, "
        print(main_menu)

        user_input = get_input("Quit", menu_dict["Quit"])
        if user_input == -1:
            # Program exiting due to EOF, KeyboardInterrupt, or "quit"
            return
        elif user_input.title() in menu_dict:
            # User passed menu option as words
            pass
        elif user_input in menu_dict_rev:
            # User passed menu option as number, set to words
            user_input = menu_dict_rev[user_input]
        else:
            # User passed unrecognized selection
            print("Unrecognized selection, please try again.")
            continue

        if user_input == "Get Users":
            print("\n", get_users(users), "\n", sep="")

        elif user_input == "New User":
            print(
                "User Account creation mode:",
                "\n" "Provide name and age by 'first:last:age': (B for back)",
                "\n",
                "ex. 'John:Smith:21'",
                "\n",
                sep="",
            )
            user_input = get_input("B")
            if user_input == -1:
                continue
            try:
                f_name, l_name, age = user_input.split(":")
            except ValueError:
                print(
                    "\n",
                    "Incorrect number of values provided, ",
                    back_to_menu,
                    "\n",
                    sep="",
                )
                continue
            try:
                age = int(age)
                if 0 > age > 120:
                    print(
                        "\n",
                        "Invalid age supplied, ",
                        back_to_menu,
                        "\n",
                        sep="",
                    )
                    continue
            except (ValueError, TypeError):
                print("\n", "Invalid age field, ", back_to_menu, "\n", sep="")
                continue
            users.append(customer.Customer(f_name, l_name, age))
            print("\n", "User account added successfully.", "\n", sep="")

        elif user_input == "Select User":
            print(
                "\n",
                get_users(users),
                "\n\n",
                "Enter a User_ID from the above list: (B for back)",
                "\n",
                sep="",
            )
            default_error = "Invalid ID, "
            return_code = select_user(users)
            if return_code == -1:
                continue
            if return_code == 0:
                print("\n", default_error, back_to_menu, "\n", sep="")
            selected_user = return_code

        elif user_input == "Display Accounts":
            if not selected_user:
                print("\n", default_error, back_to_menu, sep="")
                continue
            print(get_account_printout(selected_user))

        elif user_input in ("Withdraw", "Deposit"):
            if not selected_user:
                print("\n", default_error, back_to_menu, sep="")
                continue
            transaction_type = user_input
            if user_input == "Withdraw":
                user_func = selected_user.withdraw_from
            else:
                user_func = selected_user.deposit_into
            print(get_account_printout(selected_user))
            print(
                f"{transaction_type} mode:",
                "\n" "Select account by 'type:number:amt': (B for back)",
                "\n",
                "ex. '401k:1:400.00'",
                "\n",
                sep="",
            )
            user_input = get_input("B")
            if user_input == -1:
                continue
            try:
                account_type, number, amount = user_input.split(":")
            except ValueError:
                print(
                    "\n",
                    "Incorrect number of values provided, ",
                    back_to_menu,
                    "\n",
                    sep="",
                )
                continue
            (rc, info_msg) = perform_transaction(
                account_type, number, amount, selected_user, user_func
            )
            return_messages = {
                -4: "Transaction failed",
                -3: "Invalid account type,",
                -2: "Invalid type/amount,",
                -1: "Type/Amount must be positive,",
                0: "Invalid account number,",
                1: f"{transaction_type} successful",
            }
            if info_msg:
                print(
                    "\n",
                    return_messages[rc],
                    ": ",
                    info_msg,
                    ",\n",
                    back_to_menu,
                    "\n",
                    sep="",
                )
                continue
            print("\n", return_messages[rc], " ", back_to_menu, "\n", sep="")

        elif user_input == "New Account":
            if not selected_user:
                print("\n", default_error, back_to_menu, sep="")
                continue
            print(
                "Account creation mode:",
                "\n"
                "Provide type & initial amount by 'type:amt': (B for back)",
                "\n",
                "ex. '401k:400.00'",
                "\n",
                sep="",
            )
            user_input = get_input("B")
            try:
                account_type, amount = user_input.split(":")
            except ValueError:
                print(
                    "\n",
                    "Incorrect number of values provided, ",
                    back_to_menu,
                    "\n",
                    sep="",
                )
                continue
            try:
                amount = float(amount)
                if amount < 0:
                    print(
                        "\n",
                        "Initiial amount must be positve, ",
                        back_to_menu,
                        "\n",
                        sep="",
                    )
                    continue
            except ValueError:
                print(
                    "\n",
                    "Amount must be a valid number, ",
                    back_to_menu,
                    "\n",
                    sep="",
                )
                continue
            if account_type not in account_types:
                print(
                    "\n", "Invalid account type, ", back_to_menu, "\n", sep=""
                )
                continue
            account_classes = {
                "Checking": checking.Checking,
                "Savings": savings.Savings,
                "401K": retirement.Retirement,
                "Money Market Fund": market_fund.MoneyMarket,
            }
            new_account = account_classes[account_type](amount)
            selected_user.add_account(account_type, new_account)
            print("\n", "Account added successfully.", "\n", sep="")


def main():
    opt = get_args()
    use_teller(opt)


if __name__ == "__main__":
    try:
        main()
    except (Exception, GeneratorExit, KeyboardInterrupt, SystemExit) as e:
        name = type(e).__name__
        print("Exception of type", name, "prevented program from continuing!")
