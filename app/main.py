from fastapi import FastAPI, UploadFile, File, HTTPException
from app.parser import parse_csv, get_csv_summary
from typing import List, Dict, Any

app = FastAPI(title="CSV Processor API")

@app.get("/")
async def root():
    return {"message": "CSV Processor API is running"}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    try:
        data = parse_csv(content)
        summary = get_csv_summary(content)
        return {
            "filename": file.filename,
            "summary": summary,
            "data": data[:10]  # Return first 10 rows as preview
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
