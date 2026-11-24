import json
import os

from dotenv import load_dotenv
from anthropic import Anthropic
from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

client = Anthropic()
MODEL = "claude-sonnet-5"


def validate_ai_response(response_text):
    try:
        response_text = response_text.strip()

        # Remove Markdown code fences if Claude includes them
        if response_text.startswith("```"):
            lines = response_text.splitlines()
            if lines[-1].strip() == "```":
                response_text = "\n".join(lines[1:-1]).strip()

        response = json.loads(response_text)

        if not isinstance(response, dict):
            return None

        if not isinstance(response.get("advice"), str):
            return None

        if not isinstance(response.get("recommendation"), str):
            return None

        if not response["advice"].strip():
            return None

        if not response["recommendation"].strip():
            return None

        return response

    except (json.JSONDecodeError, ValueError):
        return None


def ask_claude(question, conversation_history=None, expenses=None):
    if conversation_history is None:
        conversation_history = []

    if expenses is None:
        expenses = []

    system_prompt = (
        SYSTEM_PROMPT
        + "\n\nRecorded expenses:\n"
        + json.dumps(expenses, indent=2)
        + "\nReturn ONLY valid JSON with advice and recommendation fields."
    )

    messages = [
        {"role": message["role"], "content": message["content"]}
        for message in conversation_history
        if message["role"] in ("user", "assistant")
    ]

    if not messages:
        messages = [{"role": "user", "content": question}]

    for attempt in range(2):
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=system_prompt,
            messages=messages
        )

        response_text = "".join(
            block.text for block in response.content
            if block.type == "text"
        )

        result = validate_ai_response(response_text)

        if result is not None:
            result["status"] = "live"
            return result

        messages.extend([
            {"role": "assistant", "content": response_text},
            {
                "role": "user",
                "content": (
                    "Your previous response was invalid. "
                    "Return corrected valid JSON with advice "
                    "and recommendation fields."
                )
            }
        ])

    raise ValueError("Claude response failed validation after one retry.")


def generate_summary(conversation_history):
    if not conversation_history:
        return "No conversation is available to summarise."

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=SUMMARY_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarise this conversation:\n"
                    + json.dumps(conversation_history, indent=2)
                )
            }
        ]
    )

    return "".join(
        block.text for block in response.content
        if block.type == "text"
    )
