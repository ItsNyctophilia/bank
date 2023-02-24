#!/usr/bin/env python3
import lib.account as account
import lib.retirement as retirement
import lib.checking as checking
import lib.customer as customer
import lib.savings as savings
import lib.money_market_fund as market_fund

def main():
    r1 = retirement.Retirement(500.2)
    r2 = retirement.Retirement(430)
    c1 = checking.Checking(400.60)
    c2 = checking.Checking(867530.90)
    m1 = market_fund.MoneyMarket(101.3)
    s1 = savings.Savings(108.88)
    c = customer.Customer("Very", "Readable", 70)
    c.add_account("401k", r1)
    c.add_account("401k", r2)
    c.add_account("Checking", c1)
    c.add_account("Checking", c2)
    c.add_account("Savings", s1)
    c.add_account("Money Market Fund", m1)
    c.withdraw_from("401k", 0, 400, c.age)
    c.withdraw_from("Checking", 0, 500)
    print(c.get_all_balances())

main()