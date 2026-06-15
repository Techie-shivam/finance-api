import plotly.express as px

def spending_by_category(df):

    category_spend = (
        df.groupby("category")["debit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_spend,
        values="debit",
        names="category"
    )

    fig.show()