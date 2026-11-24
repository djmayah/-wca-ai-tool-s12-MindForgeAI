from session_manager import load_session

filename = "session_20261118_132844.json"

session = load_session(filename)

if session:
    print("\nMINDFORGE PREVIOUS SESSION")
    print("--------------------------")
    print("Date:", session["date"])

    print("\nSaved expenses:")
    for expense in session["expenses"]:
        print(expense["description"], "- KSh", expense["amount"])

    print("\nSaved conversation:")
    for message in session["conversation"]:
        print(message["role"], ":", message["content"])