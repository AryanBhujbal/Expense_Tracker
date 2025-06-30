from flask import Flask, render_template, request, redirect, url_for, Response
from io import BytesIO
import matplotlib.pyplot as plt
from tracker.storage import load_expenses, save_expenses
from tracker.expenses import ExpenseManager, Expense

app = Flask(__name__)

def get_basic_stats(manager: ExpenseManager) -> dict:
    """Compute key statistics for the expense list."""
    stats = {}
    expenses = manager.expenses
    stats['total'] = round(manager.total(), 2)
    cat_totals = manager.by_category()
    if not expenses or not cat_totals:
        stats.update({
            'most_expensive': None,
            'cheapest': None,
            'average': 0.0,
            'avg_per_month': 0.0,
            'avg_per_day': 0.0,
            'max_category': None,
            'min_category': None,
        })
        return stats
    
    stats['most_expensive'] = max(expenses, key=lambda e: e.amount)
    
    stats['cheapest'] = min(expenses, key=lambda e: e.amount)
    
    stats['average'] = round(stats['total'] / len(expenses), 2)
    
    monthly_totals = manager.trend(monthly=True)
    stats['avg_per_month'] = round((sum(monthly_totals.values()) / len(monthly_totals)) if monthly_totals else 0.0, 2)
    
    daily_totals = manager.trend(monthly=False)
    stats['avg_per_day'] = round((sum(daily_totals.values()) / len(daily_totals)) if daily_totals else 0.0, 2)
    
    max_cat = max(cat_totals.items(), key=lambda kv: kv[1])[0]
    min_cat = min(cat_totals.items(), key=lambda kv: kv[1])[0]
    stats['max_category'] = max_cat
    stats['min_category'] = min_cat
    return stats

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        note = request.form.get('note', '')
        expenses = load_expenses()
        new = Expense(date=date, category=category, amount=amount, note=note)
        expenses.append(new)
        save_expenses(expenses)
        return redirect(url_for('index'))

    expenses = load_expenses()
    manager = ExpenseManager(expenses)
    stats = get_basic_stats(manager)
    return render_template('index.html', stats=stats)

@app.route('/expenses', methods=['GET'])
def view_expenses():

    sort_by = request.args.get('sort', 'date')
    direction = request.args.get('dir', 'asc')
    raw_expenses = load_expenses()
    indexed = list(enumerate(raw_expenses))
    if sort_by == 'category':
        key_func = lambda pair: pair[1].category.lower()
    elif sort_by == 'amount':
        key_func = lambda pair: pair[1].amount
    else:
        key_func = lambda pair: pair[1].date
    reverse = (direction == 'desc')
    sorted_indexed = sorted(indexed, key=key_func, reverse=reverse)
    toggle_dir = 'desc' if direction == 'asc' else 'asc'
    return render_template('expenses.html',
                           expenses=sorted_indexed,
                           sort_by=sort_by,
                           direction=direction,
                           toggle_dir=toggle_dir)

@app.route('/expenses/add', methods=['POST'])
def add_expense_from_expenses():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    note = request.form.get('note', '')
    expenses = load_expenses()
    new = Expense(date=date, category=category, amount=amount, note=note)
    expenses.append(new)
    save_expenses(expenses)
    return redirect(url_for('view_expenses'))

@app.route('/expenses/delete/<int:index>', methods=['POST'])
def delete_expense(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
    return redirect(url_for('view_expenses'))

@app.route('/expenses/edit/<int:index>', methods=['GET', 'POST'])
def edit_expense(index):
    expenses = load_expenses()
    if not (0 <= index < len(expenses)):
        return redirect(url_for('view_expenses'))
    expense = expenses[index]
    if request.method == 'POST':
        expense.date = request.form['date']
        expense.category = request.form['category']
        expense.amount = float(request.form['amount'])
        expense.note = request.form.get('note', '')
        save_expenses(expenses)
        return redirect(url_for('view_expenses'))
    return render_template('edit.html', expense=expense, index=index)

@app.route('/chart/categories.png')
def chart_categories():
    expenses = load_expenses()
    mgr = ExpenseManager(expenses)
    data = mgr.by_category()
    fig, ax = plt.subplots(figsize=(8,5))
    cats, vals = zip(*sorted(data.items())) if data else ([], [])
    ax.bar(cats, vals)
    ax.set_title('Expenses by Category')
    ax.set_ylabel('Amount ($)')
    plt.xticks(rotation=45, ha='right')
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/chart/pie.png')
def chart_pie():
    expenses = load_expenses()
    mgr = ExpenseManager(expenses)
    data = mgr.by_category()
    fig, ax = plt.subplots(figsize=(6,6))
    labels, sizes = zip(*sorted(data.items())) if data else ([], [])
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Expense Distribution by Category')
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/chart/monthly.png')
def chart_monthly():
    expenses = load_expenses()
    mgr = ExpenseManager(expenses)
    data = mgr.trend(monthly=True)
    fig, ax = plt.subplots(figsize=(8,5))
    months, vals = zip(*sorted(data.items())) if data else ([], [])
    ax.bar(months, vals)
    ax.set_title('Monthly Total Expenses')
    ax.set_ylabel('Amount ($)')
    plt.xticks(rotation=45, ha='right')
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)