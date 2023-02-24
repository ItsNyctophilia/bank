"""Define 'MoneyMarket' class for use as a Money Market Fund banking account

Defines a balance property to hold a current
bank account balance,as well as methods to manually set that
balance, deposit a given amount of money, or withdraw a given
amount of money if the ammount of withdrawals is less then 2."""


from abc import ABC, abstractmethod
from lib.account import Account


class MoneyMarket(Account):
    """A class that represents a Money Market Fund Bank Account

    Attributes
    ----------
    balance : float
        The amount of money a given account has, rounded at
        two decimal places
    Methods
    -------
    withdraw():
        subtracts an amount from the current balance if
        customer has made less then 2 withdrawals"""

    def __init__(self, balance):
        super().__init__(balance)
        self._transaction_count = 0

    def withdraw(self, to_withdraw):
        """Withdraws money from the account

        Returns -1 if more than two transactions have occured,
        0 if withdraw exceeds current account balance,
        and otherwise 1"""
        if self._transaction_count >= 2:
            return -2
        if to_withdraw > self._balance:
            return -1
        else:
            self._balance -= to_withdraw
            self._transaction_count += 1
            return 1
