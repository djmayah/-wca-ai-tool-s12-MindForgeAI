from .config import CURRENCY


def calculate_metrics(expenses):
    if not expenses:
        return None

    total_principal = sum(float(e.get("amount", 0)) for e in expenses)
    total_fees = sum(float(e.get("tx_cost", 0)) for e in expenses)

    grand_total = sum(
        float(e.get("total_outflow", float(e.get("amount", 0)) + float(e.get("tx_cost", 0))))
        for e in expenses
    )

    category_totals = {}

    for expense in expenses:
        category = str(
            expense.get("category", "General / Uncategorized")
        ).strip().casefold()

        display_category = category.title()

        outflow = float(
            expense.get(
                "total_outflow",
                float(expense.get("amount", 0)) + float(expense.get("tx_cost", 0))
            )
        )

        category_totals[display_category] = (
            category_totals.get(display_category, 0.0) + outflow
        )

    return {
        "count": len(expenses),
        "total_principal": total_principal,
        "total_fees": total_fees,
        "grand_total": grand_total,
        "avg_spend": grand_total / len(expenses),
        "category_totals": category_totals
    }


def print_financial_report(expenses):
    print("\n==========================================")
    print("FINANCIAL ANALYTICS & CATEGORIZATION REPORT")
    print("==========================================")

    metrics = calculate_metrics(expenses)

    if not metrics:
        print("No financial records available.")
        return

    print(f"Total Transactions : {metrics['count']}")
    print(f"Principal Spend    : {CURRENCY} {metrics['total_principal']:,.2f}")
    print(f"M-Pesa/Tx Fees     : {CURRENCY} {metrics['total_fees']:,.2f}")
    print(f"Total Outflow      : {CURRENCY} {metrics['grand_total']:,.2f}")
    print(f"Average Tx Size    : {CURRENCY} {metrics['avg_spend']:,.2f}")

    print("\n--- SPENDING BY CATEGORY ---")

    for category, total in sorted(
        metrics["category_totals"].items(),
        key=lambda item: item[1],
        reverse=True
    ):
        percentage = (
            total / metrics["grand_total"] * 100
            if metrics["grand_total"] else 0
        )

        print(
            f"{category:<25} | {CURRENCY} "
            f"{total:>10,.2f} ({percentage:>5.1f}%)"
        )
