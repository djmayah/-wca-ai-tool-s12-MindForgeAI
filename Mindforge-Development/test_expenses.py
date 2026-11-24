
from expense_manager import (
    get_total_expenses,
    view_expenses,
    get_category_totals
)

print("\nMINDFORGE EXPENSE REPORT")

print("\nRecorded expenses:")
for expense in view_expenses():
    print(expense)

print("\nTotal spending: KSh", get_total_expenses())

print("\nSpending by category:")
for category, total in get_category_totals().items():
    print(category, ": KSh", total)
