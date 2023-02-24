"""Define 'Checking' class for use as a checking banking account

Defines a balance property to hold a current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money. When the
amount requested to withdraw is more then the ammount in the account
an overdraft fee is charged."""


from abc import ABC, abstractmethod
from Account import Account


class Checking(Account):
    """A class that represents a Bank Checking Account

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
        account, then an overdraft fee is charged of
        35$. The customer still owes the money the took
        that they did not have """

    def __init__(self, _balance):
        super().__init__
        self._balance = round(_balance, 2)

    def withdraw(self, to_withdraw):
        """Withdraws money from the account

        If the amount to withdraw exceeds the ammount in the account
        an overdraft fee of 35$ is aplied to the account."""
        if to_withdraw > self._balance:
            self._balance -= to_withdraw + 35
        else:
            self._balance -= to_withdraw
