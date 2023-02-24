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
            selection = input("> ")
            selection =  selection.title().strip()
            if not selection:
                continue
            if quit_string:
                if (selection == quit_string or
                    selection == str(quit_idx)):
                    return -1
            break

        except (KeyboardInterrupt, EOFError) as e:
            return -1

    return selection


def generate_default_users(users_list):
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
    legend = "(Last), (First) : (User_ID)"
    final_list = [legend, "-" * len(legend)]
    for user in users_list:
        final_list.append(f"{user.last_name}, {user.first_name} : {user.user_ID}")
    return "\n".join(final_list)

def select_user(default_error,users):
    """Returns selected user or -1 if invalid option
    
    Keyword arguments:
    default_error -- error message string
    user_input -- sanitized output from get_input
    selected_user -- valid user object to be returned 
    
    At least default_error, and users must be passed as arguments,
    otherwise the function will fail and not select a user.
    Returns selected user or -1 if the program should produce
    a value error or if the user selects an id not contained 
    in the list of users."""
    print("\n", get_users(users), "\n\n",
    "Enter a User_ID from the above list: (B for back)", 
    "\n", sep="")
    user_input = get_input("B")
    if user_input == -1:
        return -1
    try:
        user_input = int(user_input)
    except ValueError:
        print("\n", default_error, "\n", sep="")
        return -1
    if 0 < user_input <= len(users):
        selected_user = users[user_input - 1]
        return selected_user
    else:
        print("\n", default_error, "\n", sep="")
        return -1

def use_teller():
    """Primary loop for the program"""
    main_menu, menu_dict, menu_dict_rev = create_main_menu()
    users = []
    users = generate_default_users(users)
    selected_user = None

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
            print("Unrecognized selection, please try again.\n")
            continue

        if user_input == "Get Users":
            print("\n", get_users(users), "\n", sep="")

        elif user_input == "Select User":
            default_error = "Invalid ID, returning to main menu."
            return_code = select_user(default_error,users)
            if return_code == -1:
                continue
            selected_user = return_code

        elif user_input == "Display Accounts":
            default_error = "No active user account, returning to main menu."
            if not selected_user:
                print("\n", default_error, "\n", sep="")
                continue
            f_name = selected_user.first_name
            l_name = selected_user.last_name
            account_title = f"{f_name} {l_name}'s Accounts"
            print("\n", account_title, "\n", "-" * len(account_title),
                  "\n", selected_user.get_all_balances(), "\n", sep="")
            
        elif user_input in ("Withdraw", "Deposit"):
            if user_input == "Withdraw":
                user_func = selected_user.withdraw_from
            else:
                user_func = selected_user.deposit_into
            default_error = "No active user account, returning to main menu."
            if not selected_user:
                print("\n", default_error, "\n", sep="")
                continue
            f_name = selected_user.first_name
            l_name = selected_user.last_name
            account_title = f"{f_name} {l_name}'s Accounts"
            print("\n", account_title, "\n", "-" * len(account_title),
                  "\n", selected_user.get_all_balances(), "\n", sep="")
            print("Select account by 'type:number:amt': (B for back)", 
                  "\n", "ex. '401k:1:$400'", sep="")
            user_input = get_input("B")
            if user_input == -1:
                continue
            account_type, number, amount = user_input.split(":")
            print(account_type, number, amount)
            if account_type in ("Checking", "Savings", "Money Market Fund"):
                try:
                    user_func(account_type, int(number) - 1, int(amount))
                except (IndexError, TypeError):
                    print("Invalid account number, returning to main menu.")
            elif account_type == "401K":
                try:
                    user_func(account_type, int(number) - 1, 
                                                int(amount), selected_user.age)
                except (IndexError, TypeError):
                    print("Invalid account number, returning to main menu.")

def main():
    use_teller()


if __name__ == "__main__":
    # try:
        main()
    # except (Exception, GeneratorExit, KeyboardInterrupt, SystemExit) as e:
        # name = type(e).__name__
        # print("Exception of type", name, "prevented program from continuing!")
