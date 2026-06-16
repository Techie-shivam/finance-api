import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
import pandas as pd
import tempfile
import plotly.express as px

from src.parser.pdf_reader import PDFReader
from src.parser.transaction_parser import TransactionParser
from src.models.category_mapper import assign_category
from src.analytics.analyzer import FinanceAnalyzer


st.set_page_config(
    page_title="Finance Copilot",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Finance Copilot")

uploaded_file = st.file_uploader(
    "Upload Bank Statement PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())

        pdf_path = tmp_file.name

    # --------------------------
    # PDF Extraction
    # --------------------------

    reader = PDFReader(pdf_path)

    text = reader.extract_text()

    # --------------------------
    # Transaction Parsing
    # --------------------------

    parser = TransactionParser(text)

    df = parser.parse_transactions()

    if df.empty:

        st.error(
            "No transactions detected."
        )

        st.stop()

    # --------------------------
    # Categories
    # --------------------------

    df["category"] = df["description"].apply(
        assign_category
    )

    # --------------------------
    # Analytics
    # --------------------------

    analyzer = FinanceAnalyzer(df)

    total_spending = analyzer.total_spending()

    total_income = analyzer.total_income()

    current_balance = analyzer.current_balance()

    # --------------------------
    # KPI Cards
    # --------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Spending",
        f"₹{total_spending:,.0f}"
    )

    col2.metric(
        "Total Income",
        f"₹{total_income:,.0f}"
    )

    col3.metric(
        "Current Balance",
        f"₹{current_balance:,.0f}"
    )

    # --------------------------
    # Pie Chart
    # --------------------------

    st.subheader(
        "Category Wise Spending"
    )

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------
    # Top Expenses
    # --------------------------

    st.subheader(
        "Top Expenses"
    )

    st.dataframe(
        analyzer.top_transactions()
    )

    # --------------------------
    # Full Transactions
    # --------------------------

    st.subheader(
        "All Transactions"
    )

    st.dataframe(df)