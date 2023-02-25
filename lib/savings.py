"""Define 'Savings' class for use as a checking banking account

Defines a balance property to hold the current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money. When the
amount requested to withdraw is more then the amount in the account,
nothing is withdrawn."""


from abc import ABC, abstractmethod
from lib.account import Account


class Savings(Account):
    """A class that represents a Bank Savings Account

    Attributes
    ----------
    balance : float
        The amount of money a given account has, rounded at
        two decimal places
    Methods
    -------
    withdraw():
        subtracts an amount from the current balance if
        customer would withdraw more than what is in the
        account, nothing is withdrawn"""

    def __init__(self, _balance):
        super().__init__(_balance)

    def withdraw(self, to_withdraw):
        """Withdraws money from the account

        Returns negative 1 if withdraw exceeds current account
        balance otherwise returns 1"""
        if to_withdraw > self._balance:
            return -1
        else:
            self._balance -= to_withdraw
            return 1
