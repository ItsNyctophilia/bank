import unittest

from lib.retirement import Retirement


class TestRetirement(unittest.TestCase):
    def test_init(self):
        retirement = Retirement(1000)
        self.assertEqual(retirement.balance, 1000)

    def test_withdraw(self):
        retirement = Retirement(1000)

        # Test withdrawing less than account balance
        # with customer over age 67
        result = retirement.withdraw(500, 68)
        self.assertEqual(result, 1)
        self.assertEqual(retirement.balance, 500)

        # Test withdrawing more than account balance
        # with customer over age 67
        result = retirement.withdraw(700, 68)
        self.assertEqual(result, -1)
        self.assertEqual(retirement.balance, 500)

        # Test withdrawing with customer under age 67
        result = retirement.withdraw(500, 50)
        self.assertEqual(result, 0)
        self.assertEqual(retirement.balance, 500)


if __name__ == "__main__":
    unittest.main()
