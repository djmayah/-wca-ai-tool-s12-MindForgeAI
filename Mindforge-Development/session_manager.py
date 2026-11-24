
import json
import os
from datetime import datetime

SESSION_FOLDER = "sessions"


def create_session():
    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expenses": [],
        "conversation": []
    }


def save_session(session):
    os.makedirs(SESSION_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_file = os.path.join(
        SESSION_FOLDER, f"session_{timestamp}.json"
    )

    markdown_file = os.path.join(
        SESSION_FOLDER, f"session_{timestamp}.md"
    )

    with open(json_file, "w") as file:
        json.dump(session, file, indent=4)

    with open(markdown_file, "w") as file:
        file.write("# MINDFORGE SESSION\n\n")
        file.write(f"Date: {session['date']}\n\n")
        file.write("## Expenses\n\n")

        for expense in session["expenses"]:
            file.write(
                f"- {expense['description']}: "
                f"KSh {expense['amount']} "
                f"({expense['category']})\n"
            )

        file.write("\n## Conversation\n\n")

        for message in session["conversation"]:
            file.write(
                f"**{message['role']}:** "
                f"{message['content']}\n\n"
            )

        if session.get("summary"):
            file.write("## AI Session Summary\n\n")
            file.write(session["summary"] + "\n\n")

    return json_file, markdown_file


def load_session(filename):
    filepath = os.path.join(SESSION_FOLDER, filename)

    try:
        with open(filepath, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print("Session file not found.")
        return None

    except json.JSONDecodeError:
        print("Session file is damaged or invalid.")
        return None
