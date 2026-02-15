import pandas as pd
from typing import Dict, Any, List
import io

def parse_csv(content: bytes) -> List[Dict[str, Any]]:
    """
    Parses CSV content into a list of dictionaries.
    """
    try:
        df = pd.read_csv(io.BytesIO(content))
        return df.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def get_csv_summary(content: bytes) -> Dict[str, Any]:
    """
    Returns a summary of the CSV data.
    """
    try:
        df = pd.read_csv(io.BytesIO(content))
        return {
            "rows": len(df),
            "columns": list(df.columns),
            "column_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }
    except Exception as e:
        raise ValueError(f"Error summarizing CSV: {str(e)}")
