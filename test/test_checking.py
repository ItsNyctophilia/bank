#!/usr/bin/env python3
import unittest

from lib.checking import Checking


class TestChecking(unittest.TestCase):
    def test_init(self):
        checking = Checking(1000)
        self.assertEqual(checking.balance, 1000)

    def test_withdraw(self):
        checking = Checking(1000)
        # Test withdrawing less than account balance
        result = checking.withdraw(500)
        self.assertEqual(result, 1)
        self.assertEqual(checking.balance, 500)

        # Test withdrawing more than account balance,
        # but within overdraft limit
        result = checking.withdraw(700)
        self.assertEqual(result, 0)
        self.assertEqual(checking.balance, -235)

        # Test withdrawing more than account balance, beyond overdraft limit
        result = checking.withdraw(1000)
        self.assertEqual(result, -1)
        self.assertEqual(checking.balance, -235)


if __name__ == "__main__":
    unittest.main()
