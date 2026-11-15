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
SYSTEM_PROMPT = """
ROLE:
You are Mindforge, a friendly Kenyan M-Pesa expense coach.

TASK:
The user tells you what they spent, one or two items per turn.
Record each expense with a category (Food, Transport, Airtime,
Rent, Bills, Entertainment, Other). Answer questions about their
spending using everything said earlier in this conversation.

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
{
  "reply": "short friendly message to the user",
  "new_expenses": [
    {"description": "text", "amount": 0, "category": "text"}
  ],
  "total_spent": 0
}
Use an empty list for new_expenses if nothing new was recorded.
"""

# SUMMARY PROMPT (used once, at session end - after the user says "done")
SUMMARY_PROMPT = """
ROLE:
You are Mindforge, a Kenyan M-Pesa expense coach writing an
end-of-session report.

TASK:
Summarise the whole conversation: list spending by category and
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
{
  "breakdown": [{"category": "text", "total": 0}],
  "grand_total": 0,
  "savings_tips": ["tip 1", "tip 2", "tip 3"]
}
"""

def get_ai_reply(messages):
    """Send the full message list to Claude and return its text."""
    if not API_KEY or API_KEY == "your_key_here":
        return "ERROR: API key missing. Check your .env file."
    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text
    except Exception as error:
        return f"ERROR: API call failed ({error})"


# Run a simple test if this script is executed directly
if __name__ == "__main__":
    test = [{"role": "user", "content": "I spent 200 on matatu fare"}]
    print(get_ai_reply(test))