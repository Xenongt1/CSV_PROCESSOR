import pytest
import io
from app.parser import parse_csv, get_csv_summary, detect_delimiter

def test_detect_delimiter():
    assert detect_delimiter(b"name,age\nAlice,30") == ","
    assert detect_delimiter(b"name;age\nAlice;30") == ";"

def test_parse_csv_cleaning():
    # Test whitespace stripping and delimiter detection
    csv_content = b" name ; age \n Alice ; 30 \n Bob ; "
    data = parse_csv(csv_content)
    
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[0]["age"] == 30
    assert data[1]["name"] == "Bob"
    assert data[1]["age"] is None  # Missing value handling

def test_get_csv_summary_robust():
    csv_content = b"name;age\nAlice;30\nBob;"
    summary = get_csv_summary(csv_content)
    
    assert summary["rows"] == 2
    assert summary["delimiter"] == ";"
    assert summary["missing_values"]["age"] == 1
