
import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return []

    try:
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(amount, category, description):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    expense = {
        "amount": amount,
        "category": category.strip().title(),
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)

    return expense


def get_total_expenses():
    expenses = load_expenses()
    return sum(expense["amount"] for expense in expenses)


def view_expenses():
    return load_expenses()

def get_category_totals():
    expenses = load_expenses()
    totals = {}

    for expense in expenses:
        category = expense["category"].strip().title()
        amount = expense["amount"]

        totals[category] = totals.get(category, 0) + amount

    return totals
