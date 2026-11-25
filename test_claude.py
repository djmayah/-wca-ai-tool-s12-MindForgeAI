
from ai_engine.providers.claude import ClaudeProvider

def main():

    print("Connecting to Claude API...")

    # Initialize Claude
    claude = ClaudeProvider()

    # Sample financial information
    financial_data = {
        "income": 80000,
        "rent": 20000,
        "food": 15000,
        "transport": 8000,
        "shopping": 7000
    }

    # Request financial analysis
    result = claude.analyse_finances(financial_data)

    print("\nMINDFORGE AI FINANCIAL ANALYSIS")
    print("=" * 45)
    print(result)


if __name__ == "__main__":
    main()
