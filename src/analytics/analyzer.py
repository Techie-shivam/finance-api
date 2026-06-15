class FinanceAnalyzer:

    def __init__(self, df):
        self.df = df

    def total_spending(self):
        return self.df["debit"].sum()

    def total_income(self):
        return self.df["credit"].sum()

    def current_balance(self):
        return self.df["balance"].iloc[-1]

    def top_transactions(self, n=5):

        return self.df.sort_values(
            by="debit",
            ascending=False
        ).head(n)