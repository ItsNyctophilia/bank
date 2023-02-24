"""Define 'Retirement' class for use as a 401k banking account

Defines a balance property to hold a current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money if they meet
the age requirment."""

from abc import ABC, abstractmethod
from lib.account import Account


class Retirement(Account):
    """A class that represents a 401K Bank Account

    Attributes
    ----------
    balance : float
        The amount of money a given account has, rounded at
        two decimal places
    Methods
    -------
    withdraw():
        subtracts an amount from the current balance if
        customer meets the age requirments"""

    def __init__(self, balance):
        super().__init__(balance)
        self._balance = round(balance, 2)

    def withdraw(self, to_withdraw, customer_age):
        """Withdraws money from the account

        Returns -1 if withdraw exceeds current account
        balance, 0 if customer is not old enough to withdraw,
        and otherwise returns 1"""
        if customer_age < 67:
            return -2
        if to_withdraw > self._balance:
            return -1
        else:
            self._balance -= to_withdraw
            return 1
