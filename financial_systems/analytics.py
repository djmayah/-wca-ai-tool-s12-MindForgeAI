from config import CURRENCY

def calculate_metrics(expenses):
    if not expenses:
        return None

    total_principal = sum(e["amount"] for e in expenses)
    total_fees = sum(e.get("tx_cost", 0.0) for e in expenses)
    grand_total = total_principal + total_fees
    avg_spend = grand_total / len(expenses)
    fee_ratio = (total_fees / grand_total) * 100 if grand_total > 0 else 0.0

    category_totals = {}
    for e in expenses:
        cat = e["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + e["total_outflow"]

    return {
        "count": len(expenses),
        "total_principal": total_principal,
        "total_fees": total_fees,
        "grand_total": grand_total,
        "avg_spend": avg_spend,
        "fee_ratio": fee_ratio,
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
    print(f"M-Pesa/Tx Fees     : {CURRENCY} {metrics['total_fees']:,.2f} ({metrics['fee_ratio']:.1f}% of outflow)")
    print(f"Total Outflow      : {CURRENCY} {metrics['grand_total']:,.2f}")
    print(f"Average Tx Size    : {CURRENCY} {metrics['avg_spend']:,.2f}")

    print("\n--- SPENDING BY CATEGORY ---")
    sorted_cats = sorted(metrics["category_totals"].items(), key=lambda x: x[1], reverse=True)
    for cat, total in sorted_cats:
        pct = (total / metrics["grand_total"]) * 100
        print(f"{cat:<25} | {CURRENCY} {total:>10,.2f} ({pct:>5.1f}%)")
