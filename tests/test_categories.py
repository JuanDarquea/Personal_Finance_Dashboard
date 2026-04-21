from src.categories import categorize


def test_grocery_store():
    assert categorize("Whole Foods Market") == "Groceries"


def test_transport_uber():
    assert categorize("Uber Trip") == "Transport"


def test_dining_restaurant():
    assert categorize("Restaurant El Buen Sabor") == "Dining"


def test_subscription_netflix():
    assert categorize("Netflix") == "Subscriptions"


def test_income_salary():
    assert categorize("Salary Deposit") == "Income"


def test_utilities_electricity():
    assert categorize("Electricity Bill") == "Utilities"


def test_unknown_falls_back():
    assert categorize("Some Random Store XYZ") == "Other"


def test_case_insensitive():
    assert categorize("whole foods market") == "Groceries"
