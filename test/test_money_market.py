import unittest
from lib.money_market_fund import MoneyMarket


class TestMoneyMarket(unittest.TestCase):
    def test_withdraw_less_than_two_transactions(self):
        money_market = MoneyMarket(1000)
        result = money_market.withdraw(500)
        self.assertEqual(result, 1)
        self.assertEqual(money_market.balance, 500)
        result = money_market.withdraw(300)
        self.assertEqual(result, 1)
        self.assertEqual(money_market.balance, 200)

    def test_withdraw_two_transactions(self):
        money_market = MoneyMarket(1000)
        result = money_market.withdraw(500)
        self.assertEqual(result, 1)
        self.assertEqual(money_market.balance, 500)
        result = money_market.withdraw(300)
        self.assertEqual(result, 1)
        self.assertEqual(money_market.balance, 200)
        result = money_market.withdraw(100)
        self.assertEqual(result, -2)


if __name__ == "__main__":
    unittest.main()
