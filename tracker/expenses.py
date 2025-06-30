from dataclasses import dataclass, asdict
from datetime import date
from typing import List, Optional, Dict
import statistics

@dataclass
class Expense:
    date: str
    category: str
    amount: float
    note: Optional[str] = ""

class ExpenseManager:
    def __init__(self, expenses: List[Expense]):
        self.expenses = expenses

    def total(self) -> float:
        return sum(e.amount for e in self.expenses)

    def by_category(self) -> Dict[str, float]:
        cat_totals: Dict[str, float] = {}
        for e in self.expenses:
            cat_totals.setdefault(e.category, 0.0)
            cat_totals[e.category] += e.amount
        return cat_totals

    def trend(self, monthly: bool = False) -> Dict[str, float]:
        if not monthly:
            return {e.date: e.amount for e in sorted(self.expenses, key=lambda x: x.date)}
        month_totals: Dict[str, float] = {}
        for e in self.expenses:
            m = e.date[:7]
            month_totals.setdefault(m, 0.0)
            month_totals[m] += e.amount
        return month_totals

    def extremes(self) -> Dict[str, str]:
        by_cat = self.by_category()
        if not by_cat:
            return {"highest": "", "lowest": ""}
        highest = max(by_cat.items(), key=lambda x: x[1])[0]
        lowest  = min(by_cat.items(), key=lambda x: x[1])[0]
        return {"highest": highest, "lowest": lowest}
