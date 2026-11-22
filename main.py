
from financial_systems.sms_parser import parse_mpesa_sms
from financial_systems.storage import (
    load_expenses,
    save_expenses,
    is_duplicate
)
from financial_systems.analytics import print_financial_report
from ai_engine.financial_advisor import generate_financial_insights


def display_menu():
    print("\n" + "=" * 50)
    print("       MINDFORGE AI")
    print("  PERSONAL FINANCIAL INTELLIGENCE")
    print("=" * 50)
    print("1. Import M-Pesa SMS transaction")
    print("2. View financial report")
    print("3. Generate AI financial insights")
    print("4. Exit")
    print("=" * 50)


def import_mpesa_transaction():
    sms = input("\nPaste your M-Pesa confirmation SMS:\n")

    transaction = parse_mpesa_sms(sms)

    if transaction is None:
        print("\nUnable to recognise this SMS format.")
        return

    expenses = load_expenses()

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


def view_financial_report():
    expenses = load_expenses()
    print_financial_report(expenses)


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


def main():
    while True:
        display_menu()

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            import_mpesa_transaction()

        elif choice == "2":
            view_financial_report()

        elif choice == "3":
            generate_ai_report()

        elif choice == "4":
            print("\nThank you for using MindForge AI.")
            break

        else:
            print("\nInvalid selection. Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
