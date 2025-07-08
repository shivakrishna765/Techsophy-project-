import pandas as pd

def load_and_clean_data(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [col.strip().title() for col in df.columns]
    col_map = {}
    for col in df.columns:
        if col.lower() == 'date':
            col_map[col] = 'Date'
        elif col.lower() == 'description':
            col_map[col] = 'Description'
        elif col.lower() == 'category':
            col_map[col] = 'Category'
        elif col.lower() == 'amount':
            col_map[col] = 'Amount'
    df = df.rename(columns=col_map)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Date', 'Amount'])
    df['Category'] = df['Category'].astype(str).str.title().str.strip()
    df.loc[df['Description'].str.contains('Spotify', case=False, na=False), 'Category'] = 'Entertainment'
    df.loc[df['Description'].str.contains('Starbucks', case=False, na=False), 'Category'] = 'Food'
    return df