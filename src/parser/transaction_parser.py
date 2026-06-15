import pandas as pd


class TransactionParser:

    def __init__(self, text):
        self.text = text

    def parse_transactions(self):

        transactions = []

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            if "|" not in line:
                continue

            parts = [p.strip() for p in line.split("|")]

            if len(parts) != 5:
                continue

            try:

                transactions.append({
                    "date": parts[0],
                    "description": parts[1],
                    "debit": float(parts[2]),
                    "credit": float(parts[3]),
                    "balance": float(parts[4])
                })

            except ValueError:
                continue

        return pd.DataFrame(transactions)