import pandas as pd
import os
from typing import Dict, Any

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates key performance indicators from the dataset.
    """
    kpis = {}
    
    # Financial KPIs
    if 'salary' in df.columns:
        kpis['total_payroll'] = float(df['salary'].sum())
        kpis['avg_salary'] = float(df['salary'].mean())
        kpis['salary_budget_utilization'] = float((df['salary'].sum() / (len(df) * 150000)) * 100) # Assuming 150k max
        
    if 'sale_amount' in df.columns:
        kpis['total_sales'] = float(df['sale_amount'].sum())
        kpis['avg_sale_value'] = float(df['sale_amount'].mean())
        
    # Operational KPIs
    if 'performance_score' in df.columns:
        kpis['avg_performance'] = float(df['performance_score'].mean())
        kpis['top_performers_count'] = int(len(df[df['performance_score'] >= 4.5]))
        
    kpis['total_records'] = int(len(df))
    
    return kpis

if __name__ == "__main__":
    sample_path = "data/large_sample.csv"
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        kpis = calculate_kpis(df)
        print("--- Key Performance Indicators ---")
        for k, v in kpis.items():
            print(f"{k.replace('_', ' ').title()}: {v:,.2f}" if isinstance(v, float) else f"{k.replace('_', ' ').title()}: {v}")
    else:
        print(f"Sample data not found at {sample_path}")
