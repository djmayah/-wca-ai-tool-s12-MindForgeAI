
from financial_systems.analytics import calculate_metrics
from financial_systems.config import CURRENCY
from ai_engine.providers.claude import ClaudeProvider


def generate_financial_insights(expenses):
    """
    Generate AI-powered financial insights using verified
    metrics calculated by the Python analytics engine.
    """

    if not expenses:
        return "No financial records available for analysis."

    # Step 1: Calculate metrics using Python
    metrics = calculate_metrics(expenses)

    if not metrics:
        return "Unable to calculate financial metrics."

    # Step 2: Prepare structured financial information
    financial_data = {
        "currency": CURRENCY,
        "transaction_count": metrics["count"],
        "total_principal": metrics["total_principal"],
        "total_fees": metrics["total_fees"],
        "total_outflow": metrics["grand_total"],
        "average_transaction": metrics["avg_spend"],
        "fee_percentage": metrics["fee_ratio"],
        "spending_by_category": metrics["category_totals"]
    }

    # Step 3: Send verified metrics to Claude
    advisor = ClaudeProvider()

    return advisor.analyse_finances(financial_data)
