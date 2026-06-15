import pandas as pd
import joblib
from sklearn.metrics import classification_report

df = pd.read_csv("data/training/transactions.csv")
model = joblib.load("src/models/category_model.pkl")

preds = model.predict(df["description"])
print(classification_report(df["category"], preds))