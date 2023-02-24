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
        self.assertEqual(self.customer.user_ID, 1)
        self.assertDictEqual(
            self.customer._accounts,
            {
                "Checking": [],
                "Savings": [],
                "401K": [],
                "Money Market Fund": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
