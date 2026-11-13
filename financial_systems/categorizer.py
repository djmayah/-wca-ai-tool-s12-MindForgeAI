from config import CATEGORY_RULES, DEFAULT_CATEGORY

def auto_categorize(description):
    if not description:
        return DEFAULT_CATEGORY
    
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
            
    return DEFAULT_CATEGORY
