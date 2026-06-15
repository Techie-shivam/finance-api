from src.parser.pdf_reader import PDFReader
from src.parser.transaction_parser import TransactionParser

from src.analytics.analyzer import FinanceAnalyzer

from src.models.predict_category import predict_category

from src.utils.file_utils import save_text
from src.utils.csv_utils import save_dataframe


# =====================================
# STEP 1: READ PDF
# =====================================

pdf_path = "data/raw/statement.pdf"

reader = PDFReader(pdf_path)

text = reader.extract_text()

print("\nPDF Extraction Completed")


# =====================================
# STEP 2: SAVE RAW TEXT
# =====================================

save_text(
    text,
    "data/processed/raw_text.txt"
)

print("\nRaw text saved")


# =====================================
# STEP 3: PARSE TRANSACTIONS
# =====================================

parser = TransactionParser(text)

df = parser.parse_transactions()

if df.empty:
    print("No transactions found.")
    exit()

print("\nTransactions Extracted")
print(df.head())


# =====================================
# STEP 4: ML CATEGORY PREDICTION
# =====================================

df["category"] = df["description"].apply(
    predict_category
)

print("\nCategories Predicted")

print(
    df[
        ["description", "category"]
    ].head(10)
)


# =====================================
# STEP 5: SAVE TRANSACTIONS CSV
# =====================================

save_dataframe(
    df,
    "data/processed/transactions.csv"
)

print("\nTransactions CSV Saved")


# =====================================
# STEP 6: ANALYTICS
# =====================================

analyzer = FinanceAnalyzer(df)

print("\n" + "=" * 50)
print("FINANCIAL SUMMARY")
print("=" * 50)

print(
    f"Total Spending: ₹{analyzer.total_spending():,.2f}"
)

print(
    f"Total Income: ₹{analyzer.total_income():,.2f}"
)

print(
    f"Current Balance: ₹{analyzer.current_balance():,.2f}"
)


# =====================================
# STEP 7: TOP EXPENSES
# =====================================

print("\nTOP 5 EXPENSES")

print(
    analyzer.top_transactions()
)


# =====================================
# STEP 8: CATEGORY SUMMARY
# =====================================

print("\nCATEGORY WISE SPENDING")

category_summary = (
    df.groupby("category")["debit"]
    .sum()
    .sort_values(ascending=False)
)

print(category_summary)


# =====================================
# STEP 9: SAVE CATEGORY SUMMARY
# =====================================

summary_df = (
    category_summary
    .reset_index()
)

summary_df.columns = [
    "Category",
    "Amount"
]

save_dataframe(
    summary_df,
    "data/processed/category_summary.csv"
)

print("\nCategory Summary Saved")


# =====================================
# STEP 10: MODEL PREDICTION EXAMPLES
# =====================================

print("\nMODEL TESTS")

sample_transactions = [
    "SWIGGY ORDER",
    "UBER TRIP",
    "AMAZON PURCHASE",
    "NETFLIX SUBSCRIPTION",
    "SALARY CREDIT"
]

for transaction in sample_transactions:

    prediction = predict_category(
        transaction
    )

    print(
        f"{transaction} --> {prediction}"
    )


print("\nProject Pipeline Completed Successfully!")