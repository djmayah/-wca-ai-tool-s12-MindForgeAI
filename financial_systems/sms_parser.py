import re
from models import Transaction
from categorizer import auto_categorize

def parse_mpesa_sms(sms_text):
    tx_id_match = re.search(r"^([A-Z0-9]{10})\s+Confirmed", sms_text.strip())
    amount_match = re.search(r"Ksh([\d,]+\.\d{2})\s+(?:sent to|paid to)", sms_text, re.IGNORECASE)
    recipient_match = re.search(r"(?:sent to|paid to)\s+(.+?)\s+(?:on|for account)", sms_text, re.IGNORECASE)
    cost_match = re.search(r"Transaction cost,\s*Ksh([\d,]+\.\d{2})", sms_text, re.IGNORECASE)
    date_match = re.search(r"on\s+(\d{1,2}/\d{1,2}/\d{2,4})", sms_text)

    if not (tx_id_match and amount_match):
        return None

    tx_id = tx_id_match.group(1)
    amount = float(amount_match.group(1).replace(",", ""))
    recipient = recipient_match.group(1).strip() if recipient_match else "Unknown Merchant"
    tx_cost = float(cost_match.group(1).replace(",", "")) if cost_match else 0.0
    tx_date = date_match.group(1) if date_match else None
    category = auto_categorize(recipient)

    return Transaction(
        tx_id=tx_id,
        description=recipient,
        amount=amount,
        tx_cost=tx_cost,
        category=category,
        date=tx_date,
        source="M-PESA SMS"
    )
