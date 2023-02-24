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


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except (Exception, GeneratorExit, KeyboardInterrupt, SystemExit) as e:
        name = type(e).__name__
        print("Exception of type", name, "prevented program from continuing!")
