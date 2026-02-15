import pandas as pd
import io
import csv
from typing import Dict, Any, List, Union
import os

def detect_delimiter(content: Union[bytes, str]) -> str:
    """
    Detects the delimiter of a CSV file using csv.Sniffer.
    """
    try:
        if isinstance(content, str):
            with open(content, 'rb') as f:
                raw_data = f.read(1024)
        else:
            raw_data = content[:1024]
            
        if not raw_data:
            raise ValueError("The provided CSV file is empty.")
            
        sample = raw_data.decode('utf-8')
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except Exception:
        return ','

def parse_csv(content: Union[bytes, str], filter_col: str = None, filter_val: Any = None) -> List[Dict[str, Any]]:
    """
    Parses CSV content (bytes or file path) into a list of dictionaries with optional filtering.
    """
    try:
        delimiter = detect_delimiter(content)
        
        if isinstance(content, str):
            df = pd.read_csv(content, sep=delimiter)
        else:
            df = pd.read_csv(io.BytesIO(content), sep=delimiter)
        
        # Clean data: strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Clean data: strip whitespace from all string elements
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Attempt to convert to numeric types
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
        
        # Apply filtering if requested
        if filter_col and filter_col in df.columns:
            # Convert filter_val to appropriate type if possible
            try:
                if df[filter_col].dtype in ['int64', 'float64']:
                    filter_val = float(filter_val)
            except (ValueError, TypeError):
                pass
            df = df[df[filter_col] == filter_val]
            
        # Convert to dict and handle missing values (NaN -> None)
        records = df.to_dict(orient="records")
        return [
            {k: (v if pd.notnull(v) else None) for k, v in record.items()}
            for record in records
        ]
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def get_csv_summary(content: Union[bytes, str]) -> Dict[str, Any]:
    """
    Returns an advanced summary of the CSV data.
    """
    try:
        delimiter = detect_delimiter(content)
        
        if isinstance(content, str):
            df = pd.read_csv(content, sep=delimiter)
        else:
            df = pd.read_csv(io.BytesIO(content), sep=delimiter)
            
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df = df.apply(pd.to_numeric, errors='ignore')

        stats = {}
        for col in df.columns:
            col_data = df[col]
            if pd.api.types.is_numeric_dtype(col_data):
                stats[col] = {
                    "mean": round(float(col_data.mean()), 2) if not col_data.empty else 0,
                    "median": round(float(col_data.median()), 2) if not col_data.empty else 0,
                    "min": float(col_data.min()) if not col_data.empty else 0,
                    "max": float(col_data.max()) if not col_data.empty else 0
                }
            else:
                stats[col] = {
                    "unique_count": int(col_data.nunique()),
                    "top_values": col_data.value_counts().head(3).to_dict()
                }

        return {
            "rows": len(df),
            "columns": list(df.columns),
            "delimiter": delimiter,
            "column_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "advanced_stats": stats
        }
    except Exception as e:
        raise ValueError(f"Error summarizing CSV: {str(e)}")
