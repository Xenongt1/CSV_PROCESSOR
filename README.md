# CSV Processor Pro

Advanced CSV processing API with automated delimiter detection, data cleaning, and statistical analytics.

## Features

- **FastAPI Backend**: Interactive docs at `/docs`.
- **Analytics**: Mean, median, min, max, and categorical analysis.
- **Filtering**: Query-based filtering in `/upload`.
- **JSON Export**: Download processed data via `/export/json`.
- **CI/CD**: Automated testing via GitHub Actions.

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn app.main:app --reload
```

### 3. Generate Sample Data

```bash
python scripts/generate_sample.py
```

## API Usage

### Upload & Filter

```bash
# Upload and filter by Engineering department
curl -X POST "http://localhost:8000/upload?filter_col=department&filter_val=Engineering" \
     -F "file=@data/sample.csv"
```

### Export to JSON

```bash
curl -X POST "http://localhost:8000/export/json" \
     -F "file=@data/sample.csv" \
     -o output.json
```
