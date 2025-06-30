import argparse
from .storage import load_expenses, save_expenses
from .expenses import Expense, ExpenseManager
from .visualize import plot_by_category, plot_trend

def main():
    p = argparse.ArgumentParser(prog="expense-tracker")
    sub = p.add_subparsers(dest="cmd", required=True)

    # add
    a = sub.add_parser("add")
    a.add_argument("--date", required=True)
    a.add_argument("--category", required=True)
    a.add_argument("--amount", required=True, type=float)
    a.add_argument("--note", default="")

    # total
    sub.add_parser("total")

    # by-category
    sub.add_parser("by-category")

    # trend
    t = sub.add_parser("trend")
    t.add_argument("--monthly", action="store_true")

    # extremes
    sub.add_parser("extremes")

    plot = sub.add_parser("plot", help="Show charts of your expenses")
    plot.add_argument(
        "what",
        choices=["categories", "trend"],
        help="Type of chart: 'categories' for a bar chart by category, 'trend' for a time series"
    )
    plot.add_argument(
        "--monthly",
        action="store_true",
        help="(only for 'trend') aggregate by month instead of daily"
    )

    args = p.parse_args()
    expenses = load_expenses()
    mgr = ExpenseManager(expenses)

    if args.cmd == "add":
        new = Expense(date=args.date, category=args.category,
                      amount=args.amount, note=args.note)
        expenses.append(new)
        save_expenses(expenses)
        print(f"Added: {new}")
    elif args.cmd == "total":
        print(f"Total expenses: ${mgr.total():.2f}")
    elif args.cmd == "by-category":
        for cat, amt in mgr.by_category().items():
            print(f"{cat}: ${amt:.2f}")
    elif args.cmd == "trend":
        tr = mgr.trend(monthly=args.monthly)
        for k, v in tr.items():
            print(f"{k}: ${v:.2f}")
    elif args.cmd == "extremes":
        ex = mgr.extremes()
        print(f"Highest-spend category: {ex['highest']}")
        print(f"Lowest-spend category: {ex['lowest']}")
    elif args.cmd == "plot":
        if args.what == "categories":
            plot_by_category(expenses)
        else:  # trend
            plot_trend(expenses, monthly=args.monthly)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
