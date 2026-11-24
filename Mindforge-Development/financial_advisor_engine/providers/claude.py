import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# Load the existing project-level environment file safely.
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class ClaudeProvider:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

        if not api_key:
            raise ValueError("Anthropic API key is missing.")

        self.client = Anthropic(api_key=api_key)

    def analyse_finances(self, financial_data):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are MINDFORGE's financial intelligence assistant.

Analyse these verified financial metrics:
{financial_data}

Provide:
1. Financial summary.
2. Spending patterns.
3. Financial risks.
4. Savings opportunities.
5. Practical recommendations.

Do not invent financial figures.
"""
                }
            ]
        )

        text_blocks = [
            block.text for block in response.content
            if block.type == "text"
        ]

        if not text_blocks:
            raise ValueError("Claude returned no text response.")

        return "\n".join(text_blocks)
