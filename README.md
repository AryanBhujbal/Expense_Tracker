# Simple Expense Tracker

## Features

* **Manage expenses**: Add, edit, delete, and sort expense entries (date, category, amount, note).
* **Summaries & Stats**:
  * Total spending
  * Category breakdowns
  * Most/least expensive purchases
  * Categories with highest/lowest spending
  * Average expense, average spending per month, average spending per day
* **Visualization**:

  * Bar chart: spending by category
  * Pie chart: category distribution by spending
  * Bar chart: monthly totals
* **Interfaces**:

  * **CLI**: fast terminal-based commands for power users
  * **Web app (Flask)**: interactive dashboard and table view

## Prerequisites

* Python 3.9+
* `pip` package manager
---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/AryanBhujbal/Expense_Tracker.git
   cd tracker
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

* **Data file**: `data/expenses.json` holds all expense records.
* **Generate random data** (500 entries):

  ```bash
  python3 generate_data.py
  ```
* **Require environment variable** (for Flask):

  ```bash
  export FLASK_APP=app.py
  ```

---

## Generating Data

Use the provided script to populate `data/expenses.json` with 500 random expenses:

```bash
python3 generate_data.py
```

This will create or overwrite the JSON file with sample data spanning Jan 2024–Jun 2025.

---

## Usage

### Command Line arguments 

Run all commands from the project root directory:

```bash
# Add an expense
python3 -m tracker.cli add \
  --date 2025-06-30 \
  --category Groceries \
  --amount 23.45 \
  --note "lunch"

# View total spending
python3 -m tracker.cli total

# Breakdown by category
python3 -m tracker.cli by-category

# Monthly trends
python3 -m tracker.cli trend --monthly

# Highest & lowest expense categories
python3 -m tracker.cli extremes

# Generate bar chart
python3 -m tracker.cli plot categories
```

### Web Dashboard (Flask)

1. **Start the server**

   ```bash
   flask run
   ```
2. **Navigate to** `http://127.0.0.1:5000/`

**Dashboard** (`/`):

* Form for adding new expenses
* Summary stats
* Links to charts and full table

**All Expenses** (`/expenses`):

* Sort by Date, Category, or Amount
* Form for adding new expenses
* Edit and delete options for each expense row

**Charts**:

* Bar: `/chart/categories.png`
* Pie: `/chart/pie.png`
* Bar (monthly): `/chart/monthly.png`

---

## Project Structure

```
├── app.py                    # Flask web app
├── data/
│   └── expenses.json         # JSON data
├── generate_data.py          # generate random expenses
├── tracker/                  
│   ├── __init__.py
│   ├── cli.py                # command line
│   ├── expenses.py           # classes for expense "data structure"
│   ├── storage.py            # JSON mangement
│   └── visualize.py          # matplotlib charting
├── templates/                # Flask webpage templates
│   ├── index.html
│   ├── expenses.html
│   └── edit.html
├── tests/               
│   └── test_expenses.py
└── requirements.txt          # dependencies
```

---

## Testing

Run the automated tests with Pytest:

```bash
pytest -v
```

* **Covers**: `ExpenseManager` methods (`total`, `by_category`, `trend`, `extremes`)
