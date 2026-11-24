import json
import os
# ==========================================
# MINDFORGE
# M-PESA EXPENSE COACH
# Main Python Application
# ==========================================

# Store all expenses in a list
expenses = []
DATA_FILE = "expenses.json"


def load_expenses():
    global expenses

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                expenses = json.load(file)
        except (json.JSONDecodeError, OSError):
            expenses = []
    else:
        expenses = []

load_expenses()

def save_expenses():
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# Function to record a new expense
def record_expense():

    print("\n--- RECORD EXPENSE ---")

    description = input("What did you spend money on? ")

    try:
        amount = float(input("Enter amount in KSh: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        category = input("Enter expense category: ")

        expense = {
            "description": description,
            "amount": amount,
            "category": category
        }

        expenses.append(expense)

        print("\nExpense recorded successfully!")

    except ValueError:
        print("Please enter a valid amount.")


# Function to display all expenses
def view_expenses():

    print("\n--- YOUR EXPENSES ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    for expense in expenses:
        print(
            f"{expense['description']} - "
            f"KSh {expense['amount']:.2f} - "
            f"{expense['category']}"
        )


# Function to calculate total spending
def calculate_total():

    total = 0

    for expense in expenses:
        total += expense["amount"]

    print(f"\nTotal spending: KSh {total:.2f}")

load_expenses()
# Main application menu
def main():

    while True:

        print("\n==============================")
        print(" MINDFORGE - M-PESA EXPENSE COACH")
        print("==============================")

        print("1. Record expense")
        print("2. View expenses")
        print("3. Calculate total")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            record_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            calculate_total()

        elif choice == "4":
            print("Thank you for using Mindforge!")
            break

        else:
            print("Invalid choice. Try again.")


# Start the application
if __name__ == "__main__":
    main()
