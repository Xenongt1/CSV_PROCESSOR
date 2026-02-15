import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sample_csv(filename: str, num_rows: int = 100):
    """
    Generates a sample CSV file with various data types.
    """
    departments = ["Engineering", "Marketing", "Sales", "HR", "Product", "Support"]
    data = []
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_rows):
        row = {
            "id": i + 1,
            "name": f"Employee_{i + 1}",
            "email": f"employee_{i + 1}@example.com",
            "department": random.choice(departments),
            "salary": random.randint(50000, 150000),
            "join_date": (start_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "is_active": random.choice([True, False]),
            "performance_score": round(random.uniform(1.0, 5.0), 1)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Successfully generated {num_rows} rows in {filename}")

if __name__ == "__main__":
    import os
    output_path = os.path.join("data", "large_sample.csv")
    generate_sample_csv(output_path, num_rows=1000)
