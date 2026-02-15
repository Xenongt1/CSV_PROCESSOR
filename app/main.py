import logging
import json
import tempfile
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from app.parser import parse_csv, get_csv_summary, get_cleaned_df
from app.database import save_df_to_mysql
from typing import List, Dict, Any, Optional
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("csv-processor")

app = FastAPI(
    title="CSV Processor Pro",
    description="Advanced CSV processing API with analytics, filtering, and JSON export.",
    version="2.0.0"
)

@app.get("/", tags=["Health"])
async def root():
    logger.info("Health check requested")
    return {"message": "CSV Processor API is running", "version": "2.0.0"}

@app.get("/info", tags=["System"])
async def get_info():
    """
    Returns system and API metadata.
    """
    logger.info("System info requested")
    return {
        "app_name": "CSV Processor Pro",
        "version": "2.0.0",
        "author": "Antigravity",
        "environment": os.getenv("ENV", "development"),
        "status": "operational"
    }

@app.post("/upload", tags=["Processing"])
async def upload_csv(
    file: UploadFile = File(...),
    filter_col: Optional[str] = Query(None, description="Column name to filter by"),
    filter_val: Optional[str] = Query(None, description="Value to filter for"),
    save_to_db: bool = Query(False, description="Whether to save cleaned data to MySQL"),
    table_name: Optional[str] = Query(None, description="MySQL table name (defaults to filename)")
):
    logger.info(f"Uploading file: {file.filename}")
    if not file.filename.endswith('.csv'):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    try:
        data = parse_csv(content, filter_col=filter_col, filter_val=filter_val)
        summary = get_csv_summary(content)
        
        db_status = "Not saved"
        if save_to_db:
            df = get_cleaned_df(content)
            # Use provided table name or strip extension from filename
            target_table = table_name or os.path.splitext(file.filename)[0]
            save_df_to_mysql(df, target_table)
            db_status = f"Saved to table: {target_table}"
            logger.info(db_status)
        
        logger.info(f"Successfully processed {file.filename} with {len(data)} filtered rows")
        return {
            "filename": file.filename,
            "db_status": db_status,
            "filter_applied": {"column": filter_col, "value": filter_val} if filter_col else None,
            "summary": summary,
            "data": data[:10]  # Return first 10 rows as preview
        }
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/export/json", tags=["Processing"])
async def export_to_json(file: UploadFile = File(...)):
    logger.info(f"Exporting to JSON: {file.filename}")
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    try:
        data = parse_csv(content)
        
        # Create a temporary file for the JSON export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(data, tmp, indent=4)
            tmp_path = tmp.name
            
        logger.info(f"JSON export created for {file.filename} at {tmp_path}")
        return FileResponse(
            tmp_path, 
            media_type='application/json', 
            filename=f"{os.path.splitext(file.filename)[0]}.json"
        )
    except Exception as e:
        logger.error(f"Failed to export {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
