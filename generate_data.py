#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


ENTRIES = 500
OUT = Path(__file__).parent / "data" / "expenses.json"

CATEGORIES = [
    "Groceries", "Transportation", "Entertainment", "Utilities",
    "Dining", "Healthcare", "Clothing", "Education", "Misc."
]

NOTES = [
    "Client expense", "Monthly bill", "Routine expense",
    "Personal expense", "Subscription", "Misc.", "Unknown"
]

START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2025, 6, 30)
DELTA_DAYS = (END_DATE - START_DATE).days

def generate(n = ENTRIES):
    expenses = []
    for _ in range(n):
        dt = START_DATE + timedelta(days=random.randint(0, DELTA_DAYS))
        entry = {
            "date": dt.date().isoformat(),
            "category": random.choice(CATEGORIES),
            "amount": round(random.uniform(0.5, 1000.0), 2),
            "note": random.choice(NOTES)
        }
        expenses.append(entry)
    return expenses

def main():
    data = generate()
    OUT.parent.mkdir(exist_ok=True) 
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(data)} random expenses to {OUT}")

if __name__ == "__main__":
    main()
