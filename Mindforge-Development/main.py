import json
import os

from conversation import add_message, get_history, clear_history
from session_manager import create_session, save_session, load_session
from expense_manager import (
    add_expense,
    view_expenses,
    get_total_expenses,
    get_category_totals
)
from ai_engine import ask_claude, generate_summary

from financial_systems.sms_parser import parse_mpesa_sms
from financial_systems.models import Transaction
from financial_systems.storage import save_expenses, is_duplicate
from financial_systems.analytics import print_financial_report
from financial_advisor_engine.financial_advisor import generate_financial_insights



def main():
    current_session = create_session()
    current_session["expenses"] = view_expenses()

    while True:
        print("\n===== MINDFORGE =====")
        print("M-PESA EXPENSE COACH")
        print("1. Record an expense")
        print("2. View all expenses")
        print("3. Calculate total spending")
        print("4. View spending by category")
        print("5. Exit")
        print("6. Ask MINDFORGE AI")
        print("7. Save current session")
        print("8. Open previous session")
        print("9. Import M-PESA SMS")
        print("10. View financial analytics report")
        print("11. Generate AI financial insights")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount (KSh): "))
                category = input("Enter category: ").strip()
                description = input("Enter description: ").strip()

                if not category or not description:
                    print("Category and description cannot be empty.")
                    continue

                expense = add_expense(amount, category, description)
                current_session["expenses"].append(expense)

                print("Expense recorded successfully!")

            except ValueError as error:
                print("Invalid input:", error)

        elif choice == "2":
            expenses = view_expenses()

            if not expenses:
                print("No expenses recorded yet.")
            else:
                for expense in expenses:
                    print(
                        expense["description"],
                        "- KSh", expense["amount"],
                        "-", expense["category"]
                    )

        elif choice == "3":
            print("Total spending: KSh", get_total_expenses())

        elif choice == "4":
            totals = get_category_totals()

            if not totals:
                print("No expenses recorded yet.")
            else:
                for category, total in totals.items():
                    print(category, ": KSh", total)

        elif choice == "5":
            print("Thank you for using MINDFORGE!")
            break

        elif choice == "6":
            question = input(
                "Ask MINDFORGE anything about your spending: "
            ).strip()

            if not question:
                print("Please enter a question.")
                continue

            add_message("user", question)

            current_session["conversation"].append({
                "role": "user",
                "content": question
            })

            try:
                response = ask_claude(
                    question,
                    get_history(),
                    current_session["expenses"]
                )

                assistant_content = (
                    f"Advice: {response['advice']}\n"
                    f"Recommendation: {response['recommendation']}"
                )

                                # Store the raw JSON in the history sent to Claude, so it
                # keeps replying in JSON. The readable text is only used
                # for the saved session file.
                add_message("assistant", json.dumps({
                    "advice": response["advice"],
                    "recommendation": response["recommendation"]
                }))

                current_session["conversation"].append({
                    "role": "assistant",
                    "content": assistant_content
                })

                print("\nMINDFORGE AI COACH")
                print("Advice:", response["advice"])
                print("Recommendation:", response["recommendation"])

                print("\nConversation messages:", len(get_history()))

            except Exception as error:
                # Covers no internet, a bad API key, or JSON that failed
                # the check after the retry. The program must not crash.
                # Remove the failed question from both lists so the user
                # can try again without a broken history.
                get_history().pop()
                current_session["conversation"].pop()

                if "Connection" in type(error).__name__:
                    print("\nCould not reach the AI. Check your internet "
                          "connection and try again.")
                else:
                    print("\nAI response error:", error)

        elif choice == "7":
            # Nothing to save if no AI conversation has happened yet
            if not current_session["conversation"]:
                print("Nothing to save yet. Ask the AI something first (option 6).")
                continue

            try:
                current_session["summary"] = generate_summary(
                    current_session["conversation"]
                )

                print("\nMINDFORGE AI SESSION SUMMARY")
                print(current_session["summary"])

                json_file, markdown_file = save_session(current_session)

                print("\nMINDFORGE SESSION SAVED!")
                print("JSON file:", json_file)
                print("Markdown file:", markdown_file)

            except Exception as error:
                # Covers a failed summary call as well as file errors
                print("Could not save session:", error)

        elif choice == "8":
            if not os.path.isdir("sessions"):
                print("No previous sessions found.")
                continue

            session_files = sorted(
                [
                    file for file in os.listdir("sessions")
                    if file.endswith(".json")
                ],
                reverse=True
            )

            if not session_files:
                print("No previous sessions found.")
                continue

            print("\nPREVIOUS SESSIONS")

            for index, filename in enumerate(session_files, start=1):
                print(index, filename)

            try:

                selection = int(
                    input("\nEnter session number to open: ")
                )

                if 1 <= selection <= len(session_files):
                    filename = session_files[selection - 1]
                    loaded_session = load_session(filename)

                    if loaded_session is not None:
                        current_session = loaded_session

                        clear_history()

                        for message in current_session.get("conversation", []):
                            add_message(
                                message["role"],
                                message["content"]
                            )

                        print("\nSESSION OPENED SUCCESSFULLY!")
                        print("Date:", current_session.get("date", "Unknown"))

                        print("\nSaved Expenses:")

                        for expense in current_session.get("expenses", []):
                            print(
                                expense["description"],
                                "- KSh", expense["amount"],
                                "-", expense["category"]
                            )

                        print("\nSaved Conversation:")

                        for message in current_session.get("conversation", []):
                            print(
                                message["role"],
                                ":",
                                message["content"]
                            )

                else:
                    print("Invalid session number.")

            except ValueError:
                print("Please enter a valid number.")

            except (KeyError, TypeError) as error:
                print("Could not display session:", error)

        elif choice == "9":
            sms_text = input("\\nPaste the complete M-PESA confirmation SMS:\\n").strip()

            transaction = parse_mpesa_sms(sms_text)

            if transaction is None:
                print("SMS not recognised. Please check the message format.")
                continue

            expenses = view_expenses()

            if is_duplicate(expenses, transaction.tx_id):
                print("This M-PESA transaction has already been recorded.")
                continue

            expenses.append(transaction.to_dict())
            save_expenses(expenses)
            current_session["expenses"] = expenses

            print("M-PESA transaction imported successfully!")
            print("Transaction ID:", transaction.tx_id)
            print("Description:", transaction.description)
            print("Amount: KSh", transaction.amount)
            print("Transaction fee: KSh", transaction.tx_cost)
            print("Total outflow: KSh", transaction.total_outflow)
            print("Category:", transaction.category)

        elif choice == "10":
            print_financial_report(view_expenses())

        elif choice == "11":
            try:
                expenses = view_expenses()
                print("\\nGenerating MINDFORGE financial insights...")
                insights = generate_financial_insights(expenses)
                print("\\nMINDFORGE FINANCIAL INSIGHTS")
                print(insights)

            except Exception as error:
                print("Could not generate financial insights:", error)

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
