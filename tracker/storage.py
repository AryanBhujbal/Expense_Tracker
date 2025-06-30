import json
from pathlib import Path
from .expenses import Expense
from dataclasses import asdict

DATA_FILE = Path(__file__).parent.parent / "data" / "expenses.json"

def load_expenses() -> list[Expense]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text())
    return [Expense(**r) for r in raw]

def save_expenses(expenses: list[Expense]) -> None:
    raw = [asdict(e) for e in expenses]
    DATA_FILE.write_text(json.dumps(raw, indent=2))
