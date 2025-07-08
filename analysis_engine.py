import pandas as pd
from sklearn.ensemble import IsolationForest

def summarize_by_category(df):
    return df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

def summarize_by_month(df):
    df['Month'] = df['Date'].dt.to_period('M')
    return df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)

def detect_anomalies(df):
    model = IsolationForest(contamination=0.1, random_state=42)
    df = df.copy()
    df['anomaly'] = model.fit_predict(df[['Amount']])
    anomalies = df[df['anomaly'] == -1]
    exclude_categories = ['Utilities', 'Cash']
    exclude_keywords = ['Bill', 'Withdrawal']
    mask = ~(
        anomalies['Category'].isin(exclude_categories) |
        anomalies['Description'].str.contains('|'.join(exclude_keywords), case=False, na=False)
    )
    anomalies = anomalies[mask]
    return anomalies 