"""Define 'Customer' abstract class for use as a user's banking profile

Defines relevant fields such as the user's name, age, user_id, as
well as a dictionary of all of their held accounts by type. Methods
to withdraw from and deposit to the specified account are provided."""


class Customer():
    """A class that represents a bank account-holder

    Class Variables
    ---------------
    ID : monotonically-increasing identification number

    Attributes
    ----------
    first_name : str
        customer's first name
    last_name : str
        customer's last name
    age : int
        customer's age in years
    user_id : int
        customer's unique ID
    accounts : dict
        dictionary containing '[Account Type] : [Acc1, Acc2, Acc3...]'
        (where Acc is a sub-class instance derived from Account)
        pairings that make up all of a given user's accounts

    Methods
    -------
    withdraw_from():
        subtracts an amount from the given account's current balance
    deposit_into():
        adds an amount to the given account's current balance"""

    id = 1

    def __init__(self, first_name, last_name, age):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._user_id = Customer.id
        self._accounts = {"Checking": [], "Savings": [],
                          "401K": [], "Money Market Fund": []}
        Customer.id += 1

    @property
    def first_name(self):
        """A customer's first name"""
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Set customer's first name"""
        self._first_name = first_name

    @property
    def last_name(self):
        """A customer's last name"""
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Set customer's last name"""
        self._last_name = last_name

    @property
    def age(self):
        """A customer's age in years"""
        return self._age

    @age.setter
    def age(self, age):
        """Set a customer's age"""
        self._age = age

    @property
    def user_id(self):
        """A customer's unique user ID number"""
        return self._user_id

    def list_accounts_of_type(self, account_type):
        """Returns string containing balances for given account type"""
        final_listing = []
        for idx, account in enumerate(self._accounts[account_type], 1):
            account_num = f"{account_type} #{idx}"
            account_balance = f"{self._accounts[account_type][idx - 1]}"
            account_statement = "\n".join([account_num, account_balance])
            final_listing.append(account_statement)
        return "\n\n".join(final_listing)

    def get_all_balances(self):
        """Returns string containing balances for all accounts"""
        final_listing = []
        for account_type in self._accounts.keys():
            if not self._accounts[account_type]:
                # Skip empty account types
                continue
            account_listing = self.list_accounts_of_type(account_type)
            final_listing.append(account_listing)
        return "\n\n".join(final_listing)

    def add_account(self, account_type, account):
        """Adds an Account object of given type to accounts dict"""
        self._accounts[account_type].append(account)

    def deposit_into(self, account_type, idx, amount):
        """Adds money to the specified account"""
        rc = self._accounts[account_type][idx].deposit(amount)
        return rc

    def withdraw_from(self, account_type, idx, amount, age=None):
        """Subtracts money from the specified account"""
        if age:
            rc = self._accounts[account_type][idx].withdraw(amount, age)
        else:
            rc = self._accounts[account_type][idx].withdraw(amount)
        return rc
