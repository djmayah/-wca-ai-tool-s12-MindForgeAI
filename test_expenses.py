
from expense_manager import add_expense, get_total_expenses, view_expenses

# Record two sample expenses
add_expense(200, "Food", "Lunch")
add_expense(500, "Transport", "Taxi")

# Display all expenses
print("\nMINDFORGE EXPENSE REPORT")

for expense in view_expenses():
    print(expense)

# Display total spending
print("\nTotal spending: KSh", get_total_expenses())
