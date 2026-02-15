import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations(df: pd.DataFrame, output_dir: str = "visuals"):
    """
    Generates and saves visualizations from the dataset.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    sns.set_theme(style="whitegrid")
    
    # 1. Salary Distribution by Department
    if 'salary' in df.columns and 'department' in df.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='department', y='salary', palette="viridis")
        plt.title("Salary Distribution by Department")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/salary_by_dept.png")
        plt.close()
        
    # 2. Performance Scores Distribution
    if 'performance_score' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['performance_score'], kde=True, color="skyblue")
        plt.title("Employee Performance Score Distribution")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/performance_dist.png")
        plt.close()
        
    # 3. Employee Count by City (Top 10)
    if 'city' in df.columns:
        plt.figure(figsize=(12, 6))
        df['city'].value_counts().head(10).plot(kind='bar', color='salmon')
        plt.title("Top 10 Cities by Employee Count")
        plt.ylabel("Number of Employees")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_cities.png")
        plt.close()

if __name__ == "__main__":
    sample_path = "data/large_sample.csv"
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        print("Generating visualizations...")
        generate_visualizations(df)
        print("Visualizations saved in 'visuals/' directory.")
    else:
        print(f"Sample data not found at {sample_path}")
