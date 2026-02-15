import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List, Dict, Any

# Database URL configuration
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "rootpassword")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "csv_processor")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def save_df_to_mysql(df: pd.DataFrame, table_name: str):
    """
    Saves a Pandas DataFrame to a MySQL table.
    Creates the table if it doesn't exist.
    """
    try:
        # Use pandas to_sql for efficient insertion
        # if_exists='append' allows adding to existing tables
        # index=False avoids creating a separate index column
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        return True
    except Exception as e:
        raise Exception(f"Failed to save data to MySQL: {str(e)}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
