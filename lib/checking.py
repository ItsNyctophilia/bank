"""Define 'Checking' class for use as a checking banking account

Defines a balance property to hold a current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money. When the
amount requested to withdraw is more then the amount in the account,
an overdraft fee is charged."""


from abc import ABC, abstractmethod
from lib.account import Account


class Checking(Account):
    """A class that represents a bank checking account

    Attributes
    ----------
    balance : float
        The amount of money a given account has, rounded at
        two decimal places
    Methods
    -------
    withdraw():
        subtracts an amount from the current balance, if
        customer withdraws more than what is in the
        account, then an overdraft fee of $35 is charged
        on top of the withdrawl, up to $500 over the balance"""

    def __init__(self, balance):
        super().__init__(balance)
        self._balance = round(balance, 2)

    def withdraw(self, to_withdraw):
        """Withdraws money from the account

        If the amount to withdraw exceeds the amount in the account,
        an overdraft fee of $35 is applied to the account. Returns
        -1 if the overdraft limit is exceeded, 0 if account
        overdrafted successfully, and otherwise 1."""
        if to_withdraw > self._balance:
            if to_withdraw - self._balance > 500:
                return -1
            else:
                self._balance -= to_withdraw + 35
                return 0
        else:
            self._balance -= to_withdraw
            return 1
