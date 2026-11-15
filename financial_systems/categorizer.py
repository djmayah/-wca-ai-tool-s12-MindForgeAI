
from .config import CATEGORY_RULES, DEFAULT_CATEGORY


def categorize_expense(description):
    """
    Automatically classify an expense using transaction keywords.
    """

    if not description:
        return DEFAULT_CATEGORY

    desc_lower = description.strip().lower()

    for category, keywords in CATEGORY_RULES.items():
        if any(keyword.lower() in desc_lower for keyword in keywords):
            return category

    return DEFAULT_CATEGORY


# Backward compatibility with the original function name
def auto_categorize(description):
    return categorize_expense(description)
