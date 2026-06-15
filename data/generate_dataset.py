import pandas as pd
import random

data = []

categories = {
    "Food": [
        "SWIGGY ORDER",
        "ZOMATO ORDER",
        "DOMINOS PIZZA",
        "BURGER KING",
        "KFC ORDER"
    ],

    "Travel": [
        "UBER TRIP",
        "OLA CAB",
        "RAPIDO RIDE",
        "METRO RECHARGE"
    ],

    "Shopping": [
        "AMAZON PURCHASE",
        "FLIPKART ORDER",
        "MYNTRA ORDER",
        "AJIO PURCHASE"
    ],

    "Entertainment": [
        "NETFLIX SUBSCRIPTION",
        "SPOTIFY PREMIUM",
        "YOUTUBE PREMIUM",
        "HOTSTAR PREMIUM"
    ],

    "Bills": [
        "ELECTRICITY BILL",
        "WATER BILL",
        "GAS BILL",
        "MOBILE RECHARGE"
    ],

    "Income": [
        "SALARY CREDIT",
        "FREELANCE PAYMENT",
        "INTERNSHIP STIPEND"
    ]
}

for category, merchants in categories.items():

    for _ in range(1000):

        transaction = random.choice(merchants)

        data.append({
            "description": transaction,
            "category": category
        })

df = pd.DataFrame(data)

df.to_csv(
    "data/training/transactions.csv",
    index=False
)

print(df.shape)
print("Dataset Saved")