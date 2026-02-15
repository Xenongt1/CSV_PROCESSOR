import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_sample_csv(filename: str, num_rows: int = 100):
    """
    Generates a sample CSV file with realistic data using Faker.
    """
    fake = Faker()
    departments = ["Engineering", "Marketing", "Sales", "HR", "Product", "Support"]
    data = []
    
    for i in range(num_rows):
        row = {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "job_title": fake.job(),
            "company": fake.company(),
            "department": random.choice(departments),
            "salary": random.randint(50000, 150000),
            "join_date": fake.date_between(start_date='-5y', end_date='today').strftime("%Y-%m-%d"),
            "city": fake.city(),
            "phone": fake.phone_number(),
            "is_active": random.choice([True, False]),
            "performance_score": round(random.uniform(1.0, 5.0), 1)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Successfully generated {num_rows} rows in {filename} using Faker")

if __name__ == "__main__":
    import os
    output_path = os.path.join("data", "large_sample.csv")
    generate_sample_csv(output_path, num_rows=1000)
