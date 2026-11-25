
from financial_systems.categorizer import categorize_expense


def test_food_expense():
    assert categorize_expense("Naivas Supermarket") == "Food & Groceries"


def test_transport_expense():
    assert categorize_expense("Uber Trip") == "Transport & Fuel"


def test_fuel_expense():
    assert categorize_expense("Shell Petrol Station") == "Transport & Fuel"


def test_utilities_expense():
    assert categorize_expense("Kenya Power KPLC") == "Utilities & Bills"


def test_health_expense():
    assert categorize_expense("Goodlife Pharmacy") == "Health & Pharmacy"


def test_unknown_expense():
    assert categorize_expense("Unknown transaction") == "General / Uncategorized"


def test_empty_description():
    assert categorize_expense("") == "General / Uncategorized"



