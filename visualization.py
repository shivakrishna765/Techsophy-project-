import matplotlib.pyplot as plt
import seaborn as sns

def plot_category_spending(category_summary):
    plt.figure(figsize=(8,5))
    sns.barplot(x=category_summary.values, y=category_summary.index, palette='viridis')
    plt.xlabel('Total Spend')
    plt.ylabel('Category')
    plt.title('Spending by Category')
    plt.tight_layout()
    plt.show()

def plot_monthly_trends(monthly_summary):
    plt.figure(figsize=(10,6))
    monthly_summary.plot(kind='bar', stacked=True)
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Monthly Spending Trends')
    plt.tight_layout()
    plt.show() 