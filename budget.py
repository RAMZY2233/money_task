#!/usr/bin/env python3
"""Simple monthly budget tool

Usage: run without arguments to see a sample report.
Optional: pass --input <json-file> with income and expenses.

The script prints a category breakdown, monthly savings, and a 12-month projection.
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import sys


def D(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


SAMPLE = {
    "currency": "USD",
    "monthly_income": "4000",
    "expenses": {
        "rent": "1200",
        "groceries": "400",
        "utilities": "150",
        "transport": "120",
        "subscriptions": "50",
        "entertainment": "150",
        "misc": "100"
    },
    "monthly_savings_goal": "500"
}


def load_input(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return json.loads(p.read_text())


def compute_report(data: dict) -> dict:
    currency = data.get('currency', 'USD')
    income = D(data['monthly_income'])
    expenses = {k: D(v) for k, v in data.get('expenses', {}).items()}
    total_expenses = sum(expenses.values(), D('0'))
    savings_goal = D(data.get('monthly_savings_goal', '0'))
    disposable = income - total_expenses
    monthly_savings = min(savings_goal, max(D('0'), disposable))
    surplus = disposable - monthly_savings

    # 12-month projection assuming constant monthly_savings
    projection = []
    balance = D('0')
    for m in range(1, 13):
        balance += monthly_savings
        projection.append({'month': m, 'balance': balance})

    return {
        'currency': currency,
        'income': income,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'disposable': disposable,
        'monthly_savings_goal': savings_goal,
        'monthly_savings': monthly_savings,
        'surplus_after_savings': surplus,
        'projection_12m': projection
    }


def print_report(r: dict):
    cur = r['currency']
    print('\nMonthly Budget Report')
    print('---------------------')
    print(f"Income: {r['income']} {cur}")
    print('\nExpenses:')
    for k, v in r['expenses'].items():
        print(f"  {k:14} {v} {cur}")
    print(f"  {'-'*14} {'-'*8}")
    print(f"  {'Total':14} {r['total_expenses']} {cur}")
    print('\nSummary:')
    print(f"  Disposable (income - expenses): {r['disposable']} {cur}")
    print(f"  Savings goal: {r['monthly_savings_goal']} {cur}")
    print(f"  Monthly savings (planned/possible): {r['monthly_savings']} {cur}")
    print(f"  Surplus after savings: {r['surplus_after_savings']} {cur}")
    print('\n12-month savings projection:')
    for p in r['projection_12m']:
        print(f"  Month {p['month']:2}: {p['balance']} {cur}")
    print('')


def main(argv):
    if len(argv) >= 2 and argv[1] in ('-h', '--help'):
        print(__doc__)
        return 0

    data = None
    if len(argv) >= 3 and argv[1] in ('-i', '--input'):
        try:
            data = load_input(argv[2])
        except Exception as e:
            print(f"Error loading input: {e}")
            return 2
    else:
        data = SAMPLE

    report = compute_report(data)
    print_report(report)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
