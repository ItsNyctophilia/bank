"""Define 'Savings' class for use as a checking banking account

Defines a balance property to hold a current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money. When the
amount requested to withdraw is more then the ammount in the account
Nothing is withdrawn."""


from abc import ABC, abstractmethod
from Account import Account


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
        customer withdraws more than what is in the
        account then nothing is withdrawn"""

    def __init__(self, _balance):
        super().__init__
        self._balance = round(_balance, 2)

    def withdraw(self, to_withdraw):
        """Withdraws money from the account

        Returns negetive 1 if withdraw exceeds current account
        balance otherwise returns 1"""
        if to_withdraw > self._balance:
            return (-1)
        else:
            self._balance -= to_withdraw
            return(1)
