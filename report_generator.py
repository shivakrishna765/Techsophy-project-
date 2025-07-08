import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader

# Helper to save charts as images
def save_category_pie_chart(category_summary, filename):
    expenses = category_summary[category_summary < 0].abs()
    plt.figure(figsize=(6,6))
    expenses.plot.pie(autopct='%1.1f%%')
    plt.ylabel('')
    plt.title('Spending by Category')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def save_monthly_bar_chart(monthly_summary, filename):
    plt.figure(figsize=(10,6))
    monthly_summary.plot(kind='bar', stacked=True)
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Monthly Spending Trends')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def generate_report(df, category_summary, monthly_summary, anomalies, recommendations, budget=None, output_dir='report_output'):
    os.makedirs(output_dir, exist_ok=True)
    # Save charts
    pie_chart_path = os.path.join(output_dir, 'category_pie.png')
    bar_chart_path = os.path.join(output_dir, 'monthly_bar.png')
    save_category_pie_chart(category_summary, pie_chart_path)
    save_monthly_bar_chart(monthly_summary, bar_chart_path)
    # User summary
    total_income = df[df['Amount'] > 0]['Amount'].sum()
    total_expenses = -df[df['Amount'] < 0]['Amount'].sum()
    savings = total_income - total_expenses
    # Budget comparison
    budget_comparison = None
    if budget is not None:
        budget_comparison = []
        for cat, limit in budget.items():
            spent = category_summary.get(cat, 0)
            budget_comparison.append({'category': cat, 'spent': spent, 'budget': limit, 'diff': limit - spent})
    # Render HTML
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')
    html = template.render(
        total_income=total_income,
        total_expenses=total_expenses,
        savings=savings,
        monthly_summary=monthly_summary,
        category_summary=category_summary,
        pie_chart_path=pie_chart_path,
        bar_chart_path=bar_chart_path,
        anomalies=anomalies,
        budget_comparison=budget_comparison,
        recommendations=recommendations
    )
    html_path = os.path.join(output_dir, 'finance_report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_path 