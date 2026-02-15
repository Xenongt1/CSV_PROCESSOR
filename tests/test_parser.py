import pytest
from app.parser import parse_csv, get_csv_summary

def test_parse_csv():
    csv_content = b"name,age\nAlice,30\nBob,25"
    data = parse_csv(csv_content)
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == 25

def test_get_csv_summary():
    csv_content = b"name,age\nAlice,30\nBob,25\nCharlie,"
    summary = get_csv_summary(csv_content)
    assert summary["rows"] == 3
    assert "name" in summary["columns"]
    assert summary["missing_values"]["age"] == 1
