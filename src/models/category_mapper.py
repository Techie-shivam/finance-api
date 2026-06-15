CATEGORY_MAP = {

    "SWIGGY": "Food",
    "ZOMATO": "Food",

    "UBER": "Travel",
    "OLA": "Travel",

    "AMAZON": "Shopping",
    "FLIPKART": "Shopping",

    "NETFLIX": "Entertainment",
    "SPOTIFY": "Entertainment"
}
def assign_category(description):

    description = description.upper()

    for merchant, category in CATEGORY_MAP.items():

        if merchant in description:
            return category

    return "Other"