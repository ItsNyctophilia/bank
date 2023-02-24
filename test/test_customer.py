import unittest

from lib.customer import Customer
from lib.checking import Checking
from lib.savings import Savings


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("John", "Doe", 30)

    def test_init(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.age, 30)
        self.assertEqual(self.customer.user_ID, 4)
        self.assertDictEqual(
            self.customer._accounts,
            {
                "Checking": [],
                "Savings": [],
                "401K": [],
                "Money Market Fund": [],
            },
        )

    def test_add_account(self):
        checking = Checking(1000)
        self.customer.add_account("Checking", checking)
        self.assertListEqual(self.customer._accounts["Checking"], [checking])

    def test_deposit_into(self):
        checking = Checking(1000)
        self.customer.add_account("Checking", checking)
        self.customer.deposit_into("Checking", 0, 500)
        self.assertEqual(checking.balance, 1500)

    def test_get_all_balances(self):
        savings = Savings(2000)
        self.customer.add_account("Savings", savings)
        result = self.customer.get_all_balances()
        expected = "Savings #1\nAccount balance: $2000.00"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
