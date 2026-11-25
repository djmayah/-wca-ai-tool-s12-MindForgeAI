# ==========================================
# MINDFORGE - M-PESA EXPENSE COACH
# Main Python Application
# ==========================================

from datetime import datetime

# Dan's financial systems modules (parsing, storage, analytics)
from financial_systems.sms_parser import parse_mpesa_sms
from financial_systems.storage import (
    load_expenses,
    save_expenses,
    is_duplicate
)
from financial_systems.analytics import print_financial_report

# Mayah's AI module (Claude insights)
from ai_engine.financial_advisor import generate_financial_insights


# ---------- MENU ----------
def display_menu():
    print("\n" + "=" * 50)
    print("       MINDFORGE AI")
    print("  PERSONAL FINANCIAL INTELLIGENCE")
    print("=" * 50)
    print("1. Import M-Pesa SMS transaction")
    print("2. Record expense manually")
    print("3. View financial report")
    print("4. Generate AI financial insights")
    print("5. Exit")
    print("=" * 50)


# ---------- IMPORT FROM SMS (Dan) ----------
def import_mpesa_transaction():
    sms = input("\nPaste your M-Pesa confirmation SMS:\n").strip()

    # Handle empty input
    if not sms:
        print("\nNo SMS entered.")
        return

    transaction = parse_mpesa_sms(sms)

    if transaction is None:
        print("\nUnable to recognise this SMS format.")
        return

    expenses = load_expenses()

    # Skip transactions that were already imported
    if is_duplicate(expenses, transaction.tx_id):
        print("\nThis transaction already exists.")
        return

    expenses.append(transaction.to_dict())
    save_expenses(expenses)

    print("\nTransaction successfully imported!")
    print(f"Transaction ID: {transaction.tx_id}")
    print(f"Description: {transaction.description}")
    print(f"Amount: KSh {transaction.amount:,.2f}")
    print(f"Transaction fee: KSh {transaction.tx_cost:,.2f}")
    print(f"Category: {transaction.category}")


# ---------- MANUAL ENTRY (Will, adapted to Dan's storage) ----------
def record_expense():
    print("\n--- RECORD EXPENSE ---")

    description = input("What did you spend money on? ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount in KSh: "))
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    category = input("Enter expense category: ").strip() or "Other"

    # Use the same fields as imported SMS transactions so the
    # report and AI insights treat both kinds of record the same way
    expense = {
        "tx_id": "MANUAL-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "description": description,
        "amount": amount,
        "tx_cost": 0.0,
        "category": category,
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)

    print("\nExpense recorded successfully!")


# ---------- FINANCIAL REPORT (Dan) ----------
def view_financial_report():
    expenses = load_expenses()
    print_financial_report(expenses)


# ---------- AI INSIGHTS (Mayah) ----------
def generate_ai_report():
    expenses = load_expenses()

    if not expenses:
        print("\nNo financial records available.")
        return

    print("\nGenerating AI financial insights...")
    print("Connecting to Claude...")

    try:
        insights = generate_financial_insights(expenses)

        print("\n" + "=" * 50)
        print("MINDFORGE AI FINANCIAL INTELLIGENCE")
        print("=" * 50)
        print(insights)

    except Exception as error:
        print("\nUnable to generate AI insights.")
        print(f"Error: {error}")


# ---------- MAIN LOOP ----------
def main():
    while True:
        display_menu()

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            import_mpesa_transaction()
        elif choice == "2":
            record_expense()
        elif choice == "3":
            view_financial_report()
        elif choice == "4":
            generate_ai_report()
        elif choice == "5":
            print("\nThank you for using MindForge AI.")
            break
        else:
            print("\nInvalid selection. Please choose 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()