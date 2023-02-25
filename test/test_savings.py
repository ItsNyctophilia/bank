import unittest

from lib.savings import Savings


class TestSavings(unittest.TestCase):
    def test_init(self):
        savings = Savings(1000)
        self.assertEqual(savings.balance, 1000)

    def test_withdraw(self):
        savings = Savings(1000)

        # Test withdrawing less than account balance
        result = savings.withdraw(500)
        self.assertEqual(result, 1)
        self.assertEqual(savings.balance, 500)

        # Test withdrawing more than account balance
        result = savings.withdraw(700)
        self.assertEqual(result, -1)
        self.assertEqual(savings.balance, 500)


if __name__ == "__main__":
    unittest.main()
