RULES: list[tuple[str, list[str]]] = [
    ("Groceries",      ["whole foods", "trader joe", "kroger", "aldi", "safeway", "publix", "supermarket"]),
    ("Transport",      ["uber", "lyft", "gas station", "shell", "bp", "chevron", "parking", "metro", "transit"]),
    ("Dining",         ["restaurant", "cafe", "mcdonald", "starbucks", "chipotle", "subway", "pizza", "burger", "taco", "sushi", "uber eats", "doordash", "grubhub"]),
    ("Subscriptions",  ["netflix", "spotify", "hulu", "disney", "amazon prime", "apple music", "youtube premium"]),
    ("Income",         ["salary", "payroll", "deposit", "direct deposit", "refund", "transfer in"]),
    ("Utilities",      ["electricity", "water bill", "gas bill", "internet", "phone bill", "insurance"]),
    ("Health",         ["pharmacy", "cvs", "walgreens", "gym", "fitness", "doctor", "dental", "medical"]),
    ("Shopping",       ["amazon", "h&m", "zara", "target", "walmart", "ebay", "etsy"]),
    ("Entertainment",  ["movie", "theater", "cinema", "concert", "ticketmaster", "steam", "playstation"]),
]


def categorize(description: str) -> str:
    """Return the category for a transaction description using keyword matching."""
    lower = description.lower()
    for category, keywords in RULES:
        if any(kw in lower for kw in keywords):
            return category
    return "Other"
