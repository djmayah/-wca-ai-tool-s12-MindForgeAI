import json
from .config import DATA_FILE


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def is_duplicate(expenses, tx_id):
    return any(
        str(exp.get("tx_id", "")).upper() == str(tx_id).upper()
        for exp in expenses
    )
