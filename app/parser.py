import pandas as pd
import io
import csv
from typing import Dict, Any, List

def detect_delimiter(content: bytes) -> str:
    """
    Detects the delimiter of a CSV file using csv.Sniffer.
    Defaults to ',' if detection fails.
    """
    try:
        sample = content[:1024].decode('utf-8')
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except Exception:
        return ','

def parse_csv(content: bytes) -> List[Dict[str, Any]]:
    """
    Parses CSV content into a list of dictionaries with cleaning.
    """
    try:
        delimiter = detect_delimiter(content)
        # Use sep=None with engine='python' for more robust delimiter detection if needed,
        # but Sniffer is already doing a good job.
        df = pd.read_csv(io.BytesIO(content), sep=delimiter)
        
        # Clean data: strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Clean data: strip whitespace from all string elements
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Attempt to convert to numeric types after cleaning whitespace
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
        
        # Convert to dict and handle missing values (NaN -> None) for JSON
        records = df.to_dict(orient="records")
        return [
            {k: (v if pd.notnull(v) else None) for k, v in record.items()}
            for record in records
        ]
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def get_csv_summary(content: bytes) -> Dict[str, Any]:
    """
    Returns a summary of the CSV data.
    """
    try:
        delimiter = detect_delimiter(content)
        df = pd.read_csv(io.BytesIO(content), sep=delimiter)
        df.columns = df.columns.str.strip()
        
        return {
            "rows": len(df),
            "columns": list(df.columns),
            "delimiter": delimiter,
            "column_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }
    except Exception as e:
        raise ValueError(f"Error summarizing CSV: {str(e)}")
