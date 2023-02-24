#!/usr/bin/env python3
"""Interact with a simulated bank teller system

This program allows the user to view and modify bank account
information for the various accounts of pre-defined customers,
as well as ones added during runtime."""

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
    menu_options = ["Get Users", "Select User", "Display Accounts",
                    "Withdraw", "Deposit", "Quit"]
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
            selection = input("\n> ")
            selection = selection.title().strip()
            if not selection:
                continue
            if quit_string:
                if (selection == quit_string or selection == str(quit_idx)):
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
    legend = "(Last), (First) : (User_ID)"
    final_list = [legend, "-" * len(legend)]
    for user in users_list:
        final_list.append((f"{user.last_name},"
                           f"{user.first_name} : {user.user_ID}"))
    return "\n".join(final_list)


def get_account_printout(selected_user):
    """Returns a formatted string of a customer's account statement"""
    f_name = selected_user.first_name
    l_name = selected_user.last_name
    account_title = f"{f_name} {l_name}'s Accounts"
    printout = "".join(("\n", account_title, "\n", "-" * len(account_title),
                       "\n", selected_user.get_all_balances(), "\n"))
    return printout


def perform_transaction(account_type, number, amount, user, user_func):
    """Calls the passed transaction function after input validation

    Keyword arguments:
    account_type -- type of account to check against below tuple
    number -- account number of given type
    amount -- amount to withdraw or deposit
    user -- the Customer whose account is being modified
    user_func -- the function (withdraw/deposit) to perform

    Performs the validation of the first three arguments to ensure
    the passed function call is safe. Returns -3 for invalid
    account type, -2 for number or amount unable to be converted
    to the correct data type, -1 for negative values, 0 for invalid
    index, and 1 for success."""
    account_types = ("Checking", "Savings", "Money Market Fund", "401K")
    if account_type not in account_types:
        # Case: invalid account type
        return -3

    try:
        number = int(number) - 1  # Index is number - 1
        amount = float(amount)
        if amount < 0 or number < 0:
            # Case: negative withdrawl/deposit amount
            return -1
        try:
            if account_type == "401K" and user_func == user.withdraw_from:
                user_func(account_type, number, amount, user.age)
            else:
                user_func(account_type, number, amount)
            return 1
        except IndexError:
            return 0

    except (TypeError, ValueError):
        # Case: unable to convert number/amount to int or float
        return -2


def use_teller():
    """Primary loop for the program"""
    # TODO: better docstring
    main_menu, menu_dict, menu_dict_rev = create_main_menu()
    users = []
    users = generate_default_users(users)
    selected_user = None
    back_to_menu = "returning to main menu."

    while True:
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

        elif user_input == "Select User":
            default_error = "Invalid ID,"
            print("\n", get_users(users), "\n\n",
                  "Enter a User_ID from the above list: (B for back)",
                  sep="")
            user_input = get_input("B")
            if user_input == -1:
                continue
            try:
                user_input = int(user_input)
            except ValueError:
                print("\n", default_error, back_to_menu, sep="")
                continue
            if 0 < user_input <= len(users):
                selected_user = users[user_input - 1]
            else:
                print("\n", default_error, "\n", sep="")
            continue

        elif user_input == "Display Accounts":
            default_error = "No active user account"
            if not selected_user:
                print("\n", default_error, back_to_menu, sep="")
                continue
            print(get_account_printout(selected_user))

        elif user_input in ("Withdraw", "Deposit"):
            default_error = "No active user account,"
            if not selected_user:
                print("\n", default_error, back_to_menu, sep="")
                continue
            transaction_type = None
            if user_input == "Withdraw":
                user_func = selected_user.withdraw_from
                transaction_type = "Withdraw"
            else:
                user_func = selected_user.deposit_into
                transaction_type = "Deposit"
            print(get_account_printout(selected_user))
            print(f"{transaction_type} mode:", "\n"
                  "Select account by 'type:number:amt': (B for back)",
                  "\n", "ex. '401k:1:$400'", sep="")
            user_input = get_input("B")
            if user_input == -1:
                continue
            try:
                account_type, number, amount = user_input.split(":")
            except ValueError:
                print("Incorrect number of values provided,", back_to_menu)
                continue
            rc = perform_transaction(account_type, number, amount,
                                     selected_user, user_func)
            return_messages = {-3: "Invalid account type,",
                               -2: "Invalid type/amount,",
                               -1: "Type/Amount must be positive,",
                               0: "Invalid account number,",
                               1: f"{transaction_type} successful,"}
            print("\n", return_messages[rc], " ", back_to_menu, "\n", sep="")


def main():
    use_teller()


if __name__ == "__main__":
    try:
        main()
    except (Exception, GeneratorExit, KeyboardInterrupt, SystemExit) as e:
        name = type(e).__name__
        print("Exception of type", name, "prevented program from continuing!")
