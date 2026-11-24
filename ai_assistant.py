# Contains RTCCO prompts and API communication
import os
from dotenv import load_dotenv
import anthropic
import json

#Loading the API KEY 
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-5-5"

#RTCCO PROMPTS
SYSTEM_PROMPT = f"""
ROLE:
You are Mindforge, a friendly Kenyan M-Pesa expense coach.

TASK:
The user tells you what they spent, one or two items per turn.
Record each expense with one category from (Transport & Fuel, Food & Groceries, 
Utilities & Bills, Airtime & Data, Health & Pharmacy, Peer Transfers,
General / Uncategorized(the user can specify).
Answer questions about their spending using everything said earlier in this conversation.

CONTEXT:
All amounts are in Kenyan Shillings (KSh). Users often copy
details from M-Pesa messages. Keep a running total in your head
from all earlier turns.

CONSTRAINTS:
- Never invent amounts or expenses the user did not mention.
- If an amount is missing or unclear, ask the user for it.
- Stay on personal spending. Politely refuse other topics.
- Do not give investment or legal advice.

OUTPUT:
Reply with valid JSON only, no extra text and no markdown, in
exactly this shape:
{{
  "reply": "short friendly message to the user",
  "new_expenses": [
    {{"description": "text", "amount": 0, "category": "text"}}
  ],
  "total_spent": 0
}}
Use an empty list for new_expenses if nothing new was recorded.
"""

# SUMMARY PROMPT (used once, at session end - after the user says "done")
SUMMARY_PROMPT = f"""
ROLE:
You are Mindforge, a Kenyan M-Pesa expense coach writing an
end-of-session report.

TASK:
Summarise the whole conversation: list spending by category
(only these categories: (Transport & Fuel, Food & Groceries, 
Utilities & Bills, Airtime & Data, Health & Pharmacy, Peer Transfers,
General / Uncategorized(the user can specify) and
give exactly three practical ways the user can save money.

CONTEXT:
You are given the full conversation. All amounts are in KSh.
Use only expenses the user actually mentioned.

CONSTRAINTS:
- Never invent amounts or categories.
- Exactly three saving tips, specific to this user's spending.
- No investment or legal advice.

OUTPUT:
Reply with valid JSON only, no extra text and no markdown:
{{
  "breakdown": [{{"category": "text", "total": 0}}],
  "grand_total": 0,
  "savings_tips": ["tip 1", "tip 2", "tip 3"]
}}
"""

def get_ai_reply(messages, system_prompt=SYSTEM_PROMPT):
    """Send the full message list to Claude and return its text."""
    if not API_KEY or API_KEY == "your_key_here":
        return "ERROR: API key missing. Check your .env file."
    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
    except Exception as error:
        return f"ERROR: API call failed ({error})"

def parse_json_reply(text):
    """Turn Claude's text into a dict. Returns {"error": ...} if it fails."""
    if text.startswith("ERROR:"):
        return {"error": text}
    try:
        return json.loads(text.strip().strip("`").removeprefix("json"))
    except json.JSONDecodeError:
        return {"error": "ERROR: Could not read the AI reply."}


# MEMORY: the conversation sent to Claude, saved and remembered even after app closes.

MEMORY_FILE = "chat_memory.json"


def load_memory():
    """Load the saved conversation (empty list if none)."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def clear_memory():
    """Start a fresh conversation."""
    history.clear()
    save_memory()


history = load_memory()


def chat(user_text):
    """Normal turn. Claude remembers everything said before.

    Returns {"reply", "new_expenses", "total_spent"} or {"error": ...}.
    """
    history.append({"role": "user", "content": user_text})
    result = parse_json_reply(get_ai_reply(history))
    if "error" in result:
        history.pop()  # failed turn is not remembered, so the user can retry
        return result
    history.append({"role": "assistant", "content": json.dumps(result)})
    save_memory()
    return result


def summary():
    """End of session. Returns {"breakdown", "grand_total", "savings_tips"}."""
    if not history:
        return {"error": "ERROR: Nothing to summarise yet."}
    messages = history + [{"role": "user", "content": "I'm done. Write my report."}]
    return parse_json_reply(get_ai_reply(messages, SUMMARY_PROMPT))


# Run a simple test if this script is executed directly
if __name__ == "__main__":
    test = [{"role": "user", "content": "I spent 200 on matatu fare"}]
    print(get_ai_reply(test))



# MINDFORGE AI ASSISTANT

# Sample AI response (replace this with your actual AI-generated response)
response = {
    "reply": "Got it! I've recorded your matatu fare of KSh 200 under Transport & Fuel. Your total spending so far is KSh 200. What else have you spent on today?",
    "new_expenses": [
        {
            "description": "Matatu fare",
            "amount": 200,
            "category": "Transport & Fuel"
        }
    ],
    "total_spent": 200
}


# DISPLAY OUTPUT

print("\n" + "=" * 40)
print("       MINDFORGE AI ASSISTANT")
print("=" * 40)


# TRANSACTION DETAILS

print("\nTRANSACTION DETAILS")
print("-" * 40)

for expense in response["new_expenses"]:
    print(f"Description : {expense['description']}")
    print(f"Amount      : KSh {expense['amount']}")
    print(f"Category    : {expense['category']}")


# DAILY SPENDING SUMMARY

print("\nDAILY SPENDING SUMMARY")
print("-" * 40)

print(f"Total Spent : KSh {response['total_spent']}")


# AI CONVERSATIONAL MESSAGE (NO HEADING)

print("\n" + response["reply"])

print("=" * 40)
