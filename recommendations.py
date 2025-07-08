def generate_recommendations(df, category_summary, anomalies):
    recs = []
    top_category = category_summary.idxmax()
    if category_summary[top_category] > 0.3 * df['Amount'].sum():
        recs.append(f"You spent a lot on {top_category}. Consider setting a budget.")
    if not anomalies.empty:
        for _, row in anomalies.iterrows():
            recs.append(f"Unusual spend detected: ${row['Amount']} at {row['Description']} on {row['Date'].date()}")
    if not recs:
        recs.append("No unusual spending detected. Good job!")
    return recs 