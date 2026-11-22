
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)


class ClaudeProvider:

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL")

        if not api_key:
            raise ValueError("Anthropic API key is missing.")

        if not self.model:
            raise ValueError("Anthropic model is missing.")

        self.client = Anthropic(api_key=api_key)

    def analyse_finances(self, financial_data):

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are MindForge AI's financial intelligence assistant.

                    Analyse the following financial information:

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

        # Extract text blocks from Claude's response
        text_blocks = [
            block.text
            for block in response.content
            if block.type == "text"
        ]

        if not text_blocks:
            raise ValueError("Claude returned no text response.")

        return "\n".join(text_blocks)
