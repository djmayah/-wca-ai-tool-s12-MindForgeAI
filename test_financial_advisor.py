
from ai_engine.financial_advisor import generate_financial_insights


def main():

    # Sample financial transactions
    expenses = [
        {
            "tx_id": "TEST000001",
            "description": "Naivas Supermarket",
            "amount": 15000.00,
            "tx_cost": 0.00,
            "total_outflow": 15000.00,
            "category": "Food & Groceries"
        },
        {
            "tx_id": "TEST000002",
            "description": "Uber Kenya",
            "amount": 5000.00,
            "tx_cost": 50.00,
            "total_outflow": 5050.00,
            "category": "Transport & Fuel"
        },
        {
            "tx_id": "TEST000003",
            "description": "Kenya Power",
            "amount": 4000.00,
            "tx_cost": 0.00,
            "total_outflow": 4000.00,
            "category": "Utilities & Bills"
        }
    ]

    print("\nMINDFORGE AI FINANCIAL ADVISOR")
    print("=" * 45)

    insights = generate_financial_insights(expenses)

    print(insights)


if __name__ == "__main__":
    main()
