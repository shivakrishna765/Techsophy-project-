import streamlit as st
from data_ingestion import load_and_clean_data
from analysis_engine import summarize_by_category, summarize_by_month, detect_anomalies
from visualization import plot_category_spending, plot_monthly_trends
from recommendations import generate_recommendations
import os
from report_generator import generate_report

st.title("Personal Finance Tracker with Spending Insights")

uploaded_file = st.file_uploader("Upload your transactions CSV", type="csv")
if uploaded_file:
    df = load_and_clean_data(uploaded_file)
    st.write("### Raw Data", df)
    category_summary = summarize_by_category(df)
    monthly_summary = summarize_by_month(df)
    anomalies = detect_anomalies(df)
    st.write("### Spending by Category")
    st.bar_chart(category_summary)
    st.write("### Monthly Spending Trends")
    st.bar_chart(monthly_summary)
    if not anomalies.empty:
        st.write("### Anomalies Detected")
        st.dataframe(anomalies[['Date', 'Description', 'Category', 'Amount']])
    st.write("### Recommendations")
    recs = generate_recommendations(df, category_summary, anomalies)
    for rec in recs:
        st.write("- " + rec)
    st.write("---")
    st.write("## Generate Report")
    if st.button("Generate Finance Report (HTML)"):
        html_path = generate_report(
            df, category_summary, monthly_summary, anomalies, recs, budget=None
        )
        with open(html_path, "r", encoding="utf-8") as f:
            st.download_button(
                label="Download HTML Report",
                data=f.read(),
                file_name="finance_report.html",
                mime="text/html"
            )
else:
    st.info("Please upload a CSV file to get started.") 