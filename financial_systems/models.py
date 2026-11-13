from datetime import datetime

class Transaction:
    def __init__(self, tx_id, description, amount, tx_cost=0.0, category="General / Uncategorized", date=None, source="MANUAL"):
        if amount <= 0:
            raise ValueError("Transaction principal amount must be greater than zero.")
        if tx_cost < 0:
            raise ValueError("Transaction cost cannot be negative.")
        if not tx_id or not str(tx_id).strip():
            raise ValueError("Transaction ID is required.")

        self.tx_id = str(tx_id).strip().upper()
        self.description = str(description).strip()
        self.amount = round(float(amount), 2)
        self.tx_cost = round(float(tx_cost), 2)
        self.total_outflow = round(self.amount + self.tx_cost, 2)
        self.category = str(category).strip()
        self.date = date if date else datetime.now().strftime("%d/%m/%y")
        self.source = source

    def to_dict(self):
        return {
            "tx_id": self.tx_id,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "tx_cost": self.tx_cost,
            "total_outflow": self.total_outflow,
            "category": self.category,
            "source": self.source
        }
