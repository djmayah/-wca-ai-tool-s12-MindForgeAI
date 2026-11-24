
from conversation import add_message, get_history, clear_history

add_message("user", "How much am I spending on food?")
add_message("assistant", "You should monitor your food expenses.")

add_message("user", "How can I reduce it?")
add_message("assistant", "Set a weekly food budget.")

print("\nMINDFORGE CONVERSATION MEMORY")
print("--------------------------------")

for message in get_history():
    print(message["role"], ":", message["content"])

print("\nTotal messages:", len(get_history()))

from session_manager import create_session, save_session

# Create a sample session
session = create_session()

# Add sample expenses
session["expenses"].append({
    "amount": 200,
    "category": "Food",
    "description": "Lunch"
})

session["expenses"].append({
    "amount": 150,
    "category": "Transport",
    "description": "Bus fare"
})

# Add sample conversation
session["conversation"].append({
    "role": "user",
    "content": "How can I reduce my spending?"
})

session["conversation"].append({
    "role": "assistant",
    "content": "Create a weekly budget."
})

# Save session
files = save_session(session)

print("MINDFORGE SESSION SAVED!")
print("JSON file:", files[0])
print("Markdown file:", files[1])
