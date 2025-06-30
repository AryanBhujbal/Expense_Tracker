import pytest
from tracker.expenses import Expense, ExpenseManager

# Sample expenses
@pytest.fixture
def sample_expenses():
    return [
        Expense("2025-06-01", "Groceries", 50.00, note="food"),
        Expense("2025-06-02", "Transport", 15.00, note="bus"),
        Expense("2025-06-15", "Groceries", 30.00, note="snacks"),
        Expense("2025-07-01", "Entertainment", 40.00, note="movies"),
        Expense("2025-07-15", "Utilities", 100.00, note="electric"),
    ]

#no expenses
@pytest.fixture
def empty_expenses():
    return []

def test_total_calculation(sample_expenses):
    manager = ExpenseManager(sample_expenses)
    assert pytest.approx(manager.total()) == 235.00

def test_total_empty(empty_expenses):
    manager = ExpenseManager(empty_expenses)
    assert manager.total() == 0.0

def test_by_category_grouping(sample_expenses):
    manager = ExpenseManager(sample_expenses)
    category_totals = manager.by_category()
    expected = {
        "Groceries": 80.00,
        "Transport": 15.00,
        "Entertainment": 40.00,
        "Utilities": 100.00,
    }
    assert category_totals == expected

def test_by_category_empty(empty_expenses):
    manager = ExpenseManager(empty_expenses)
    assert manager.by_category() == {}


def test_trend_date_sorted(sample_expenses):
    manager = ExpenseManager(sample_expenses)
    trend = manager.trend(monthly=False)
    dates = list(trend.keys())
    assert dates == sorted(dates)
    for exp in sample_expenses:
        assert trend[exp.date] == exp.amount

def test_trend_monthly(sample_expenses):
    manager = ExpenseManager(sample_expenses)
    monthly_trend = manager.trend(monthly=True)
    expected_monthly = {
        "2025-06": 95.00,
        "2025-07": 140.00,
    }
    assert monthly_trend == expected_monthly

def test_trend_empty(empty_expenses):
    manager = ExpenseManager(empty_expenses)
    assert manager.trend(monthly=False) == {}
    assert manager.trend(monthly=True) == {}

def test_extremes(sample_expenses):
    manager = ExpenseManager(sample_expenses)
    extremes = manager.extremes()
    assert extremes["highest"] == "Utilities"
    assert extremes["lowest"] == "Transport"

def test_extremes_empty(empty_expenses):
    manager = ExpenseManager(empty_expenses)
    extremes = manager.extremes()
    assert extremes["highest"] == ""
    assert extremes["lowest"] == ""
