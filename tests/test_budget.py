from decimal import Decimal
import pytest

from budget import compute_report, SAMPLE


def D(v):
    return Decimal(v).quantize(Decimal('0.01'))


def test_sample_report():
    r = compute_report(SAMPLE)
    assert r['income'] == D('4000')
    assert r['total_expenses'] == D('2170')
    assert r['monthly_savings'] == D('500')
    # last month balance: 12 * 500 = 6000
    assert r['projection_12m'][-1]['balance'] == D('6000')


def test_savings_goal_larger_than_disposable():
    data = {
        "currency": "USD",
        "monthly_income": "1000",
        "expenses": {"rent": "900"},
        "monthly_savings_goal": "500"
    }
    r = compute_report(data)
    # disposable = 100, so monthly_savings should be 100 (min(goal, disposable))
    assert r['disposable'] == D('100')
    assert r['monthly_savings'] == D('100')
    assert r['projection_12m'][0]['balance'] == D('100')
