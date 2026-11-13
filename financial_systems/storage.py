import json
import os
from config import DATA_FILE

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)

def is_duplicate(expenses, tx_id):
    return any(exp.get("tx_id") == tx_id for exp in expenses)
