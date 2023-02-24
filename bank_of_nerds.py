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
    menu selections and a dictionary with keys and values of the
    menu options for later lookups."""
    main_menu = menu.Menu()
    menu_dict = {}
    menu_options = ["Get Users", "Current User", "Display Accounts",
                    "Withdraw", "Deposit", "Quit"]
    for idx, selection in enumerate(menu_options, 1):
        main_menu.add_selection(selection)
        menu_dict.update({selection: idx})
    return (main_menu, menu_dict)


def get_input(quit_idx):
    """Returns sanitized user input or -1 if program should exit
    
    Keyword arguments:
    quit_idx -- numerical index into main menu of the quit button"""
    while True:
        try:
            selection = input("> ")
            selection =  selection.lower().strip()
            if not selection:
                continue
            elif selection == "quit" or selection == str(quit_idx):
                return -1
            break

        except (KeyboardInterrupt, EOFError) as e:
            return -1

    return selection


def use_teller():
    """Primary loop for the program"""
    main_menu, menu_dict = create_main_menu()
    while True:
        print(main_menu)
        user_input = get_input(menu_dict["Quit"])
        if user_input == -1:
            return
        


def main():
    use_teller()


if __name__ == "__main__":
    try:
        main()
    except (Exception, GeneratorExit, KeyboardInterrupt, SystemExit) as e:
        name = type(e).__name__
        print("Exception of type", name, "prevented program from continuing!")
