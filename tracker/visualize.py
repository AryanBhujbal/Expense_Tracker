import matplotlib.pyplot as plt
from .expenses import ExpenseManager
from .storage import load_expenses

def plot_by_category(expenses=None):
    if expenses is None:
        expenses = load_expenses()
    mgr = ExpenseManager(expenses)
    data = mgr.by_category()
    if not data:
        print("No data to plot.")
        return

    cats, vals = zip(*sorted(data.items(), key=lambda kv: kv[0]))
    plt.figure()
    plt.bar(cats, vals)
    plt.title("Expenses by Category")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def plot_trend(expenses=None, monthly=False):
    if expenses is None:
        expenses = load_expenses()
    mgr = ExpenseManager(expenses)
    data = mgr.trend(monthly=monthly)
    if not data:
        print("No data to plot.")
        return

    items = sorted(data.items(), key=lambda kv: kv[0])
    dates, amounts = zip(*items)
    plt.figure()
    plt.plot(dates, amounts, marker="o")
    title = "Monthly" if monthly else "Daily"
    plt.title(f"{title} Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
