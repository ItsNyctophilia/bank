"""Define 'Account' abstract class for use as a generic banking account

Defines a balance property to hold a current bank account balance,
as well as methods to manually set that balance, deposit a given
amount of money, or withdraw a given amount of money."""

from abc import ABC, abstractmethod


class Account(ABC):
    """A class that represents a generic bank account

    Attributes
    ----------
    balance : float
        The amount of money a given account has, rounded at
        two decimal places

    Methods
    -------
    withdraw():
        subtracts an amount from the current balance
    deposit():
        adds an amount to the current balance"""

    def __init__(self, _balance):
        self._balance = round(_balance, 2)

    def __str__(self):
        return f'Account balance: ${self._balance:.2f}'

    @property
    def balance(self):
        """Current account balance"""
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        """Set the balance to the specified value"""
        self._balance = round(new_balance, 2)

    def deposit(self, to_deposit):
        """Add money to the current balance, returns new balance"""
        self._balance += round(to_deposit, 2)

    @abstractmethod
    def withdraw(self, to_withdraw):
        """Subtract money from the current balance"""
        pass
