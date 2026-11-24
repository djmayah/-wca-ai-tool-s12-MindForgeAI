from pathlib import Path

CURRENCY = "KSh"
DATA_FILE = Path(__file__).resolve().parent.parent / "expenses.json"
DEFAULT_CATEGORY = "General / Uncategorized"

CATEGORY_RULES = {
    "Transport & Fuel": [
        "uber", "bolt", "little", "total", "shell", "rubis",
        "matatu", "stage", "parking", "ntsa", "super metro"
    ],
    "Food & Groceries": [
        "naivas", "carrefour", "quickmart", "kfc", "java",
        "artcaffe", "supermarket", "butchery", "mama mboga", "chandarana"
    ],
    "Utilities & Bills": [
        "kplc", "kenya power", "nairobi water", "safaricom",
        "airtel", "zuku", "wifi", "gotv", "dstv", "rent"
    ],
    "Airtime & Data": ["airtime", "bundles", "data"],
    "Health & Pharmacy": [
        "goodlife", "pharmacy", "hospital", "clinic", "chemist", "dental"
    ],
    "Peer Transfers": ["sent to", "paid to"]
}
